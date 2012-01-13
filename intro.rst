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
in Python and can be deployed on different platforms: Linux, Windows and MacOS X.

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

Get CDMI-Proxy package (RPM, DEB or MSI - depending on your distribution) from 
http://cdmi.pdc2.pdc.kth.se/downloads.

 
Configuring Backends
====================

By default *localdisk* backend is configured. If you want to use AWS or Azure,
you need to modify configuration file.

Configuration files are placed in */etc/cdmiproxy* on Linux and in the 
*etc\cdmiproxy* folder in the installed directory on Windows. 


Examples of Usage
=================

By default CDMI-Proxy opens two connections: TLS on port 8080 and HTTP on port 2365.
Both of them require authentication, which can be modified in the configuration
files. Out of the box "user:cdmipass" (for HTTP-Digest) and "aaa:aaa" (for HTTP-Basic)
are available.

cURL
----

Creating a container (CDMI):

.. code-block:: sh

  $ curl -v -H 'x-cdmi-specification-version: 1.0.1' -H 'content-type: application/cdmi-container' -H  'accept:application/cdmi-container' http://cdmiserver:2365/newcontainer
  

libcdmi (Python)
----------------
TBA

libcdmi (Java)
--------------
TBA

Troubleshooting
===============

Please, report any issues or problems to https://github.com/livenson/vcdm/issues .