CDMI-Proxy
----------

CDMI-Proxy is an implementation of a CDMI-compatible (v 1.0.1) server that can be 
used to store data both using local infrastructure and public cloud services.

See http://cdmi.pdc2.pdc.kth.se/docs/ for documentation.

Implementation supports:
 * Blobs
 * Multi-level containers (also for single-level backends, e.g. AWS or Azure)

SETUP
=====
 1. Get the code: 

    * `git clone git://github.com/livenson/vcdm.git`

 1. Get dependencies:

    * `pip install -r requirements.txt`
    * install CouchDB: http://couchdb.apache.org/  (at least version 1) 
      * Couchbase offers latest versions:  http://www.couchbase.com/downloads/couchbase-single-server/community

 1. Run start-server.sh/start-server.bat.
    * by default, ports 2364 and 8080 will be accessible.
    * 2364: debugging access - no encryption or authN
    * 8080: production access - encryption and authN

 1. Building documentation using sphinx:
    * install Sphinx: `pip install Sphinx`
    * run `makedoc.sh`

 1. There are several backends available at the moment. If you are planning to use them, you also need to get the
 corresponding libraries (and put them on the PYTHONPATH or into $vcdm/libsrc):

    * AWS: http://code.google.com/p/boto/ 
    * CDMI: https://github.com/livenson/libcdmi-python
    * Azure: https://github.com/livenson/winazurestorage

LICENSE
=======

The terms of use of the software are governed by the BSD license (3 clause).
