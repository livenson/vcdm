#!/usr/bin/python

# depends on fusepy, not python-fuse
# may conflict with python-fuse if that is installed
# in this case it would be wise to rename this module to fusepy
from collections import defaultdict
from errno import ENOENT, EPERM
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
import vcdm.blob

class CloudFS(LoggingMixIn, Operations):
    """Cloud storage FUSE filesystem plugin"""
    def __init__(self):
        self.files = {}
        self.data = defaultdict(str)
        self.fd = 0
        now = time()
        self.files['/'] = dict(st_mode=(S_IFDIR | 0755), st_ctime=now,
            st_mtime=now, st_atime=now, st_nlink=2)
        
    def chmod(self, path, mode):
        self.files[path]['st_mode'] &= 0770000
        self.files[path]['st_mode'] |= mode
        return 0

    def chown(self, path, uid, gid):
        self.files[path]['st_uid'] = uid
        self.files[path]['st_gid'] = gid
    
    def create(self, path, mode):
        self.files[path] = dict(st_mode=(S_IFREG | mode), st_nlink=1,
            st_size=0, st_ctime=time(), st_mtime=time(), st_atime=time())
        self.fd += 1
        res,a = vcdm.blob.write(path, b'') # todo: metadata support
        if res != vcdm.CREATED:
            raise FuseOSError(ENOENT)
        return self.fd
    
    def getattr(self, path, fh=None):
        if path not in self.files:
            now = time()
            return dict(st_mode=(S_IFREG | 0644), st_ctime=now, st_mtime=now, st_atime=now)
        st = self.files[path]
        return st
    
    def getxattr(self, path, name, position=0):
        attrs = self.files[path].get('attrs', {})
        try:
            return attrs[name]
        except KeyError:
            return ''       # Should return ENOATTR
    
    def listxattr(self, path):
        attrs = self.files[path].get('attrs', {})
        return attrs.keys()
    
    def mkdir(self, path, mode):
        self.files[path] = dict(st_mode=(S_IFDIR | mode), st_nlink=2,
                st_size=0, st_ctime=time(), st_mtime=time(), st_atime=time())
        self.files['/']['st_nlink'] += 1
    
    def open(self, path, flags):
        self.fd += 1
        return self.fd
    
    def read(self, path, size, offset, fh):
        #return self.data[path][offset:offset + size]
        print offset, size
        res, data = vcdm.blob.read(path, rng=(offset, offset+size))
        if res != vcdm.OK:
            raise FuseOSError(ENOENT)
        return data
    
    def readdir(self, path, fh):
        # each file entry must be a tuple or list of name, attrs and offset
        dirls = vcdm.blob.readdir(path)
        for item in dirls:
            self.files[item[0]] = dict(st_mode=(S_IFREG |
                                                int('0o'+item[1]['acl'], 0)))
        return ['.', '..'] + [(item[0].split('/')[-1], self.files[item[0]], 0)
                              for item in dirls]
        #return ['.', '..'] + [x[1:] for x in self.files if x != '/']
    
    def readlink(self, path):
        #return self.data[path]
        res, data = vcdm.blob.read(path)
        if res != vcdm.OK:
            raise FuseOSError(ENOENT)
        return data
    
    def removexattr(self, path, name):
        attrs = self.files[path].get('attrs', {})
        try:
            del attrs[name]
        except KeyError:
            pass        # Should return ENOATTR
    
    def rename(self, old, new):
        self.files[new] = self.files.pop(old)
        # TODO:persist!

    def rmdir(self, path):
        self.files.pop(path)
        self.files['/']['st_nlink'] -= 1
        # TODO:persist!
    
    def setxattr(self, path, name, value, options, position=0):
        # Ignore options
        attrs = self.files[path].setdefault('attrs', {})
        attrs[name] = value
        # TODO:persist!
    
    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)
        # TODO:persist!
    
    def symlink(self, target, source):
        self.files[target] = dict(st_mode=(S_IFLNK | 0777), st_nlink=1,
            st_size=len(source))
        self.data[target] = source
        # TODO:persist!
    
    def truncate(self, path, length, fh=None):
        self.data[path] = self.data[path][:length]
        self.files[path]['st_size'] = length
        # TODO:persist!
    
    def unlink(self, path):
        #self.files.pop(path)
        res = vcdm.blob.delete(path)
        if res != vcdm.OK:
            raise FuseOSError(ENOENT)
    
    def utimens(self, path, times=None):
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime
        # TODO:persist!
    
    def write(self, path, data, offset, fh):
        #self.data[path] = self.data[path][:offset] + data
        #self.files[path]['st_size'] = len(self.data[path])
        #return len(data)
        res, ign = vcdm.blob.write(path, (offset, offset+len(data)))
        return len(data)

if __name__ == "__main__":
    if len(argv) != 2:
        print 'usage: %s <mountpoint>' % argv[0]
        exit(1)
    fuse = FUSE(CloudFS(), argv[1], foreground=True)

