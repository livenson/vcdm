Configuration
=============

CDMI-Proxy reads in its configuration from the files in the following order:

#. /etc/cdmiproxy/vcdm-defaults.conf'
#. /etc/cdmiproxy/vcdm.conf
#. /vcdm-defaults.conf
#. ./vcdm.conf (relative to pwd) 
#. ~/.vcdm.conf

Configuration is additive, so you can overwrite separate settings in
configuration files with higher priority.

When installing using packages, configuration files are placed into
*/etc/cdmiproxy* on Linux and into *etc\\cdmiproxy* folder inside the
installation directory on Windows.

Configuring backends
====================

By default *localdisk* backend is configured. If you want to use AWS or Azure,
you need to modify configuration file.For each of the storage accounts you want
to use, create a separate configuration section and add backend type (azure or
aws) and corresponding parameters. *bucket_name* specifies a bucket name in the
corresponding storage account, where CDMI-Proxy will store its files (in order to
avoid namespace polution).

.. code-block:: sh

 [my_aws_account]
 type = aws
 credentials.username = ACCESSKEYID
 credentials.password = SECRETACCESSKEY
 aws.bucket_name = cdmi-proxy

 [my_azure_account]
 type = azure
 credentials.account = ACCOUNTNAME
 credentials.password = SECRETACCESSKEY
 azure.bucket_name = cdmi-proxy
 # don't change settings below if you don't know what they mean
 credentials.blob_url = blob.core.windows.net
 credentials.table_url = table.core.windows.net
 credentials.queue_url = queue.core.windows.net

Choosing a backend for storing a blob
=====================================

It is possible to configure more than one backend, where data gets stored, i.e. PUT on data object is called.
For example, you can store datasets for specific experiments in the backends, which are closer to the planned execution
site. When making a CDMI request, you can specify where the data should go to using either a metadata field
'desired_backend' or by setting an HTTP header 'desired_backend'. In case both are specified, metadata field takes
precedence.

For example, if you have defined backends *home* and *remote_aws*, then a sample HTTP PUT looks like this:

.. code-block:: sh

  $ curl -v -u username:pass --digest \
        -H 'desired_backend: remote_aws' \
        --data @mylocalfile
        -X PUT http://cdmiserver:2365/file_to_be_stored_in_aws

Authentication
==============

CDMI-Proxy supports two authentication schemes: HTTP-Basic and HTTP-Digest.

In order to use use HTTP-Basic authentication scheme you need to create a
file with a list of users in "username:md5hexdigest(password)" format, one entry
per line. In order to active the usage of this schema, set *usersdb.md5* in the
configuration file to point to your users list.

.. code-block:: sh

    [general] 
    usersdb.md5 = /path/to/your/usersdb/file


Using HTTP-Digest is very similar, only that the format is 
"username:plaintext_password" and the setting name is *usersdb*.


Authorization
=============

Authorization is done through authorization hooks, which accept avatar (aka user),
action, object and a set of permissions. There are two supported authorization 
methods: dummy and strict.

*Dummy* schema allows everything to everyone, use with care and only in trusted
environments.

*Strict* schema assures that avatar performing the actions has corresponding 
set of permissions on that object. 

List of actions:

#. blob_read
#. blob_write
#. blob_delete
#. container_read
#. container_write
#. container_delete
 
List of permissions (shortened version used for setting permissions through
REST calls):

#. read (r)
#. write (w)
#. delete (d)

Setting or updating permissions is done through CDMI calls. We currently do not
support the overly complicated NFSv4 ACL format defined by CDMI specification.
Instead we support a simplified format, where *metadata* field contains a 
dictionary of username-permissions mapping (the call must be performed on the
object, whose ):

.. code-block:: js

 {
   //...
   "metadata" : {
        "cdmi_acl" : { 
            "userA" : "r",
            "userB" : "rws"
        }
   },
   //...
 }

There is a special user "Anonymous", which corresponds to public access.


Accounting
==========

CDMI-Proxy reports basic accounting information (number of atomic operations, total data size at the end of the period)
to a file and optionally to an accounting server in OGF User Records (UR) format. The idea is that every period,
specified by the *accunting.total_frequency* setting in the configuration, a query is issued to the data store for the
total size of the entries indexed by CDMI-Proxy. This information, along with the number of basic operations performed
through this CDMI-Proxy instance, is then dumped to the defined targets.

In order to use UR-based reporting, you need to define to additional values in the configuration file: identity of the
UR creator (e.g. can be the same as *ur_username*) and identity of the resource owner.

The following parameters of the configuration file are relevant for accounting:

.. code-block:: sh

    [general]
    accounting_log = /path/tp/accounting/file.log

    accounting.total_frequency = 600.0
    send_accounting_to_ur = yes
    ur_server=http://accounting-host/usagetracker/rest/usagerecords/storage/
    ur_username=ur_username
    ur_password=ur_password
    ur_creator=reporter of the record
    ur_resource_owner=resource owner


Delegated user for accounting
=============================

In some cases it might be desired to specify a user who should be accounted for a certain action. For example, when a
single CDMI-Proxy account is shared between multiple users and they want to differentiate their usage.

In order to do that in CDMI-Proxy, one needs to:

1. Enable support for that in the configuration, by setting:

.. code-block:: sh

    [general] 
    use_delegated_user = yes

2. Define a special header *ONBEHALF* in the CDMI request.

.. code-block:: sh

  $ curl -v -u user_eve:pass --digest \
        -H 'onbehalf: user_alice' \
        --data @mylocalfile
        -X PUT http://cdmiserver:2365/file_to_be_stored


Examples of Usage
=================

By default CDMI-Proxy opens two connections: TLS on port 8080 and HTTP on port 2365.
Both of them require authentication, which can be modified in the configuration
files. Out of the box "user:cdmipass" (for HTTP-Digest) and "aaa:aaa" (for HTTP-Basic)
are available.

Browser
-------

You can use your every day browser to read the contents of the CDMI-Storage. 
Simply open http://URI_OF_CDMI_SERVER:port.


cURL
----

You can use `curl <http://curl.haxx.se/>`_ for constructing a valid CDMI request.
For example, to create a new container, run the following command:

.. code-block:: sh

  $ curl -v -u username:pass --digest \
        -H 'x-cdmi-specification-version: 1.0.1' \
        -H 'content-type: application/cdmi-container' \
        -H  'accept:application/cdmi-container' \
        -X PUT http://cdmiserver:2365/newcontainer

Refer to `CDMI reference <http://cdmi.sniacloud.com/>`_ for more precise
header/body specification. 

libcdmi (Python)
----------------

Using a `Python wrapper <https://github.com/livenson/libcdmi-python>`_ for CDMI
function calls, a basic workflow of a client could look like this:

.. code-block:: python

 # sample client of a CDMI service
 import tempfile
 import os
 
 from libcdmi import cdmi
 
 endpoint = "http://localhost:2364/"
 credentials = {'user': 'aaa',
                'password': 'aaa'}
 
 lf, localfile = tempfile.mkstemp()
 os.write(lf, "# Test data #")
 os.close(lf)

 remoteblob = 'test_file.txt'
 remoteblob2 = '/mydata/text_file.txt'
 
 remote_container = '/mydata'
 remote_container2 = '/mydata/more'
 
 conn = cdmi.CDMIConnection(endpoint, credentials)
 
 # blob operations
 conn.blob_proxy.create_from_file(localfile, remoteblob, mimetype='text/plain')
 conn.blob_proxy.create_from_file(localfile, remoteblob + "_nocdmi", )
 
 value = conn.blob_proxy.read(remoteblob)
 print "=== Value ==\n%s\n" % value
 
 conn.blob_proxy.delete(remoteblob)
 
 # container operations
 conn.container_proxy.create(remote_container)
 print conn.container_proxy.read('/')
 conn.container_proxy.delete(remote_container)
 print conn.container_proxy.read('/')
 
 # cleanup 
 os.unlink(localfile)


libcdmi (Java)
--------------

Using a `Java wrapper <https://github.com/livenson/libcdmi-java>`_ for CDMI
function calls, a basic workflow of a client could look like this:

.. code-block:: java

 package examples;
 
 import static eu.venusc.cdmi.CDMIResponseStatus.REQUEST_OK;
 
 import java.io.File;
 import java.net.URL;
 import java.util.HashMap;
 import java.util.LinkedList;
 import java.util.List;
 import java.util.Map;
 
 import org.apache.http.HttpResponse;
 import org.apache.http.auth.Credentials;
 import org.apache.http.auth.UsernamePasswordCredentials;
 
 import eu.venusc.cdmi.CDMIConnection;
 import eu.venusc.cdmi.Utils;
 
 public class CDMIClient {
 
    private static String cdmiBase = "/test-container-1/";
    private static String nonCdmiBase = "/test-container-2/";
    private static String outputContainer = "/test-output/";
 
    public static void main(String[] args) throws Exception {
        // user credentials
        Credentials creds = new UsernamePasswordCredentials("username",
                "password");
 
        // two CDMI-storages
        CDMIConnection localStorage = new CDMIConnection(creds, new URL(
                "https://localhost:8080"));
        CDMIConnection remoteStorage = new CDMIConnection(creds, new URL(
                "https://example.com:8080"));
 
        // CDMI blob read operations
        List<File> dataset = new LinkedList<File>();
        System.out.println("== Downloading blobs (CDMI objects) ==");
        String[] inputFiles = new String[] { "input_1.txt", "input_2.txt" };
        for (String fnm : inputFiles) {
            String location = cdmiBase + fnm;
            HttpResponse response = localStorage.getBlobProxy().read(location);
            if (response.getStatusLine().getStatusCode() != REQUEST_OK) {
                System.err.println("Download failed : " + fnm);
            }
            File localFile = Utils.createTemporaryFile(Utils
                    .getTextContent(response), fnm, null);
            System.out.println("File downloaded: "
                    + localFile.getAbsolutePath());
            dataset.add(localFile);
            response.getEntity().consumeContent(); // to free up resource
        }
 
        // Non-CDMI read data operations (on larger blobs)
        System.out.println("== Downloading blobs (non-CDMI objects) ==");
        String[] largerInputFiles = new String[] { "larger_file_1.dat",
                "larger_file_2.dat" };
        for (String fnm : largerInputFiles) {
            String location = nonCdmiBase + fnm;
            HttpResponse response = localStorage.getNonCdmiBlobProxy()
                    .read(location);
            if (response.getStatusLine().getStatusCode() != REQUEST_OK) {
                System.err.println("Download failed : " + fnm);
            }
 
            File localFile = Utils.createTemporaryFile(new String(Utils
                    .extractContents(response)), fnm, null);
            System.out.println("File downloaded: "
                    + localFile.getAbsolutePath());
            dataset.add(localFile);
            response.getEntity().consumeContent(); // to free up resource
        }
        // Process ...
 
        // ... and upload to a remote storage
        System.out
                .println("== Uploading dataset to a remote storage (CDMI objects) ==");
        for (File f : dataset) {
            // A shared map with custom parameters
            Map parameters = new HashMap();
            parameters.put("mimetype", "text/plain");
            HttpResponse response = remoteStorage.getNonCdmiBlobProxy().create(
                    outputContainer + f.getName(), f, parameters);
            if (response.getStatusLine().getStatusCode() != REQUEST_OK) {
                System.err.println("Upload failed : " + f.getName());
            }
            response.getEntity().consumeContent(); // to free up resource
        }
 
        // Check what's in the output folder - and delete it at the same time
        System.out.println("== Contents of: " + outputContainer + " ==");
 
        for (String s : remoteStorage.getContainerProxy().getChildren(
                outputContainer)) {
            System.out.println(s);
            System.out.println("\t\tDeleting...");
            remoteStorage.getBlobProxy().delete(outputContainer + s);
        }
        System.out.println("==============");
    }
 }
 

Troubleshooting
===============

Please, report any issues or problems to https://github.com/livenson/vcdm/issues .