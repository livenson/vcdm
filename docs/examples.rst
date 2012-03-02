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
