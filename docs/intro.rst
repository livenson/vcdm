Introduction
============

CDMI-Proxy is a server exposing `CDMI-compliant <http://cdmi.sniacloud.com/>`_ interface. For the actual storage of the
data several backends are available:
 
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

In order to run, CouchDB service must be installed first. CDMI-Proxy requires `CouchDB <http://couchdb.apache.org/>`_ version 1+.Please, make sure that version
requirement is met - many distributions contain older version, which will not work. You can get latest RPMs/DEBs from `Couchbase 
<http://www.couchbase.com/downloads/couchbase-single-server/community>`_. Or use a `pipeline <https://github.com/iriscouch/build-couchdb>`_ for compiling CouchDB 
from scratch.


Windows installation shortcut
-----------------------------

1. Install `Python 2.7 <http://python.org/ftp/python/2.7.2/python-2.7.2.msi>`_.

2. Install `OpenSSL <http://www.slproweb.com/download/Win32OpenSSL-1_0_0g.exe>`_ (if missing, install `VC++2008 Redistributables <http://www.microsoft.com/downloads/details.aspx?familyid=9B2DA534-3E03-4391-8A4D-074B9F2BC1BF>`_).

3. Install `CouchDB <https://github.com/downloads/dch/couchdb/setup-couchdb-1.1.1_js185_otp_R14B03+fix-win32-crypto.exe>`_.

4. Install `Twisted <http://pypi.python.org/packages/2.7/T/Twisted/Twisted-12.0.0.win32-py2.7.msi>`_.

5. Install `Setup tools <http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20>`_.

6. Open Command line (Start -> Run: cmd)

.. code-block:: bat

  > easy_install zope.interface
  > easy_install CouchDB
  > easy_install pyOpenSSL

7. Install `CDMI-Proxy <http://resources.venus-c.eu/cdmiproxy/msi/cdmiproxy-0.1-latest.msi>`_.

8. Make sure CouchDB is running and start CDMI-Proxy by running "C:\\Python27\\Scripts\\cdmipd.exe" (modify for your Python installation path).


Installation from packages
--------------------------
You can get CDMI-Proxy core and standard configurations also from packages. The latest packages (RPM,
DEB and MSI) can be downloaded from http://resources.venus-c.eu/.

Installing CDMI-Proxy package _does not_ install all of the dependencies, these must be installed manually.
Apart from CouchDB store, CDMI-Proxy requires several Python libraries, which need to be installed explicitly.
Using `pip installer <http://www.pip-installer.org/en/latest/installing.html>`_
the process looks like this on all operating systems:

.. code-block:: sh

  $ pip install zope.interface Twisted CouchDB pyOpenSSL


Source code
-----------
You can get the code from https://github.com/livenson/vcdm .