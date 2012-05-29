##
# Copyright 2002-2012 Ilja Livenson, PDC KTH
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
# Based on https://github.com/opennode/opennode-management/blob/master/opennode/oms/config.py

from ConfigParser import ConfigParser, Error as ConfigKeyError
import os
import sys

_config = None


def get_config():
    global _config
    if not _config:
        _config = VCDMConfig()
    return _config


class VCDMConfig(ConfigParser):
    """CDMI-Proxy configuration loader"""

    __default_files__ = ['/etc/cdmiproxy/vcdm-defaults.conf',
                         '/etc/cdmiproxy/vcdm-linux.conf',
                         '/etc/cdmiproxy/vcdm.conf',
                         # a slightly hackish way to include configuration location on windows for msi installs
                          os.path.join(sys.path[0], '..', 'cdmiproxy', 'vcdm-defaults.conf'),
                          os.path.join(sys.path[0], '..', 'cdmiproxy', 'vcdm-win.conf'),
                         './vcdm-defaults.conf', './vcdm.conf', '~/.vcdm.conf',
                         ]

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
