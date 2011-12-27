from setuptools import setup, find_packages


setup(
    name = "cdmiproxy",
    version = "0.1",
    description = """CDMI Proxy""",
    author = "Ilja Livenson",
    author_email = "ilja.livenson@gmail.com",
    packages = find_packages(where='src'),
    package_dir = {'': 'src'},
    install_requires = ['zope.interface', 'Twisted', 'CouchDB', 'pyOpenSSL'],
    data_files = [('/etc/cdmiproxy', ['vcdm.conf', 'vcdm.conf.template',
                                      'users.db', 'users.db.md5']),
                  ('/opt/vcdmdata', [])
                  ]
    #entry_points = {'console_scripts': ['cdmipd = :run vcdm.proxy.start ']}
)
