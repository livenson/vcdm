from setuptools import setup, find_packages
import platform
import os


data_files = [('/etc/cdmiproxy', ['vcdm.conf', 'vcdm-defaults.conf',
                                  'users.db', 'users.db.md5']),
              ('/etc/cdmiproxy/server_credentials', 
                                ['server_credentials/cert.pem', 'server_credentials/key.pem']),
              ('/opt/vcdmdata', [])]

if platform.system() == 'Windows':
    data_files = [('cdmiproxy', ['vcdm-win.conf', 'vcdm-defaults.conf', 
                                 'users.db', 'users.db.md5']),
                  (os.path.join('cdmiproxy', 'server_credentials'), 
                            ['server_credentials/cert.pem', 'server_credentials/key.pem'])]

setup(
    name = "cdmiproxy",
    version = "0.1",
    description = """CDMI Proxy""",
    author = "Ilja Livenson",
    author_email = "ilja.livenson@gmail.com",
    packages = find_packages(where='src'),
    package_dir = {'': 'src'},
    data_files = data_files,
    install_requires = ['zope.interface',
                        'Twisted',
                        'CouchDB',
                        'pyOpenSSL'],

    entry_points = {'console_scripts': ['cdmipd = vcdm.daemon:main']}
)
