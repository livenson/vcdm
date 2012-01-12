# Based on https://github.com/opennode/opennode-management/blob/master/opennode/oms/config.py

from ConfigParser import ConfigParser, Error as ConfigKeyError
import os

_config = None


def get_config():
    global _config
    if not _config:
        _config = VCDMConfig()
    return _config


class VCDMConfig(ConfigParser):
    """CDMI-Proxy configuration loader"""

    __default_files__ = ['./etc/cdmiproxy/vcdm-defaults.conf', '/etc/cdmiproxy/vcdm.conf', 
                         './vcdm-defaults.conf', './vcdm.conf', '~/.vcdm.conf']

    def __init__(self, config_filenames=__default_files__):
        ConfigParser.__init__(self)
        self.read([os.path.expanduser(i) for i in config_filenames])
        
    def getboolean(self, section, option, default=False):
        try:
            return ConfigParser.getboolean(self, section, option)
        except ConfigKeyError:
            return default

    def getint(self, section, option, default=False):
        try:
            return ConfigParser.getint(self, section, option)
        except ConfigKeyError:
            return default

    def getfloat(self, section, option, default=False):
        try:
            return ConfigParser.getfloat(self, section, option)
        except ConfigKeyError:
            return default
