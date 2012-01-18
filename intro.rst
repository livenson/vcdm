Introduction
============

CDMI-Proxy is a server exposing `CDMI-compliant <http://cdmi.sniacloud.com/>`_ 
interface. For the actual storage of the data several backends are available:
 
 * Local disk: storing contents on a POSIX filesystem.
 * AWS S3: storing contents in Amazon public cloud.
 * Azure Blob: storing content in Azure public cloud.

Metadata of the stored elements is kept in a CouchDB server.

Quick Start
===========

CDMI-Proxy is written using `Twisted network engine <http://twistedmatrix.com/>`_ 
in Python (v2.6+) and was seen working on a number of platforms: Linux, Windows
and MacOS X.

Dependencies
------------

1. In order to run, CouchDB service must be installed first. CDMI-Proxy requires 
`CouchDB <http://couchdb.apache.org/>`_ version 1+.Please, make sure that version
requirement is met - many distributions contain older version, which will not 
work. You can get latest RPMs/DEBs from `Couchbase 
<http://www.couchbase.com/downloads/couchbase-single-server/community>`_. Or use a
`pipeline <https://github.com/iriscouch/build-couchdb>`_ for compiling CouchDB 
from scratch.

2. In additiona, CDMI-Proxy requires several Python libraries. Using `pip installer
<http://www.pip-installer.org/en/latest/installing.html>`_ the process looks
like this on all operating systems:

.. code-block:: sh

  $ pip install zope.interface Twisted CouchDB pyOpenSSL

Installing on Linux/Windows
---------------------------

You can get the latest CDMI-Proxy packages (RPM, DEB or MSI - depending on your
 distribution) from http://cdmi.pdc2.pdc.kth.se/downloads.

Installing from Source
----------------------
You can get the code from https://github.com/livenson/vcdm . Follow README to
get the CDMI-Proxy up and running. 

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

Configuring Backends
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
For example:

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