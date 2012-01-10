from setuptools import setup, find_packages
import platform
import os

base_path = '/' if platform.system() == 'Linux' else '.'

setup(
    name = "cdmiproxy",
    version = "0.1",
    description = """CDMI Proxy""",
    author = "Ilja Livenson",
    author_email = "ilja.livenson@gmail.com",
    packages = find_packages(where='src'),
    package_dir = {'': 'src'},
    install_requires = ['zope.interface',
                        'Twisted',
                        'CouchDB',
                        'pyOpenSSL'],

    data_files = [(os.path.join(base_path, 'etc', 'cdmiproxy'), ['vcdm.conf', 'vcdm-defaults.conf',
                                      'users.db', 'users.db.md5']),
                  (os.path.join(base_path, 'opt', 'vcdmdata'), [])],

    entry_points = {'console_scripts': ['cdmipd = vcdm.daemon:main ']}
)
