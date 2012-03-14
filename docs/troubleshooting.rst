Troubleshooting
===============

1. Are there any errors/exceptions at the end of the CDMI-Proxy log? Unless you've redefined it's location, it should be called *vcdm.log* or *cdmiproxy.log*.

2. Is CouchDB working? By default, CouchDB console is accesible at http://localhost:5984/_utils .

3. Is *ulimit -n* of a reasonable size? Multiple connections can cause depletion of the open files limit. We suggest running CDMI-Proxy with a larger limit, e.g. 50000.

Known issues
============

1. https://issues.apache.org/jira/browse/COUCHDB-1397 breaks CouchDB on the latest Debian (seen on 6.0.4), which also breaks CDMI-Proxy.

Please, report any issues or problems to https://github.com/livenson/vcdm/issues .