CDMI-Proxy
----------

CDMI-Proxy is an implementation of a CDMI-compatible (v 1.0.1) server that can be used to store data both using local infrastructure and public cloud services. Multiplatform.

Read more [documentation](http://resources.venus-c.eu/cdmiproxy/docs/index.html) or proceed to the short setup guide below.

Currently supported CDMI objects are:
 * Blobs
 * Multi-level containers (also for single-level backends, e.g. AWS or Azure)

Currently supported backends:
 * Local disk
 * AWS S3
 * Azure Blob

SETUP
=====

### Get the code
 * git clone git://github.com/livenson/vcdm.git

### Get dependencies
 * pip install -r requirements.txt
 * install [CouchDB](http://couchdb.apache.org/)  (at least version 1) 

### Run
Run _start-server.sh_/_start-server.bat_. By default, ports 2365 (plain) and 8080 (tls) will be listening for CDMI calls.

### Build documentation
* pip install Sphinx
* makedoc.sh

### Add backends
There are several backends available at the moment. If you are planning to use them, you also need to get the
corresponding libraries (and put them on the _PYTHONPATH_ or into _libsrc_ folder):
 * [AWS](http://code.google.com/p/boto/)
 * [CDMI](https://github.com/livenson/libcdmi-python)
 * [Azure](https://github.com/livenson/pyazure)

LICENSE
=======

The terms of use of the software are governed by the Apache 2 license.

CDMI Clients
=======

 * [libcdmi (java)](https://github.com/livenson/libcdmi-java): SDK for running CDMI calls 
 * [libcdmi (python)](https://github.com/livenson/libcdmi-python): SDK for running CDMI calls
 * [cdmifs](https://github.com/koenbollen/cdmifs): FUSE based file system using the CDMI standard (v1.0).
 * [r2ad](http://r2ad.net/): demo clients for OCCI and CDMI
 * TCS CDMI Automated Test Suite(CATS): validation test suite for CDMI (contact: nishi.g@tcs.com)
 * [Scality Droplet](https://github.com/scality/Droplet) - a library from Scality with support for CDMI

(c) [Ilja Livenson](mailto:ilja.livenson@gmail.com)

