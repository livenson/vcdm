import os

backend_type = 'localdisk'

# TODO: replace with a property
loc = 'local-storage/'

def write(fnm, content):
    """Write the content to a file"""
    f = open(loc + '/' + fnm, 'w')
    status = 0 if f.closed else 0
    f.write(content)        
    f.close()

def read(fnm, rng=None):
    """Read the contents of a file, possibly a certain byte range"""
    f = open(loc + '/' + fnm, 'r')
    d = None
    if rng is None:
        d = f.read()
    else:
        f.seek(rng[0])
        d = f.read(rng[1] - rng[0])
    f.close()
    return d 

def delete(fnm):
    """Delete a specified file"""
    os.remove(loc + '/' + fnm)
    
