CDMI_VERSION = '1.0.1'
CDMI_SERVER_HEADER = "CDMI-Proxy/" + CDMI_VERSION

from itertools import groupby


def set_common_headers(request):
    request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
    request.setHeader('Server', CDMI_SERVER_HEADER)


def parse_path(path):
    """Parse request path, return (name, [container_path], fullpath) tuple. """
    fullpath = path
    # remove duplicate consecutive slashes: e.g. /// -> /
    filtered_path = [k for k, _ in groupby(fullpath.split('/')) if k != '']
    filtered_path.insert(0, '/')  # add root container

    # if we have length one, the can only be a root path. For that we define
    # container_path = ['/'], i.e. it is self-contained.
    if len(filtered_path) == 1:
        return ('/', ['/'], '/')
    else:
        return (filtered_path[-1], filtered_path[:-1],
                "/".join(filtered_path)[1:])


def get_parent(fullpath):
    """
    Parse the string and return a path corresponding to the parent.
    Assumes normalized fullpath string.
    """
    parent = "/".join(fullpath.split('/')[:-1])
    if parent == '':  # a top-level hack
        parent = '/'
    return parent


def get_common_body(request, uid, fullpath):
    """
    Return dictionary with body elements common to all/most of the
    CDMI responses.
    """
    server = request.host.host + ":" + str(request.host.port)

    body = {
            'objectID': uid,
            'domainURI': server,
            'parentURI': get_parent(fullpath),
            'objectURI': fullpath,
            'objectName': fullpath.rsplit('/')[-1]
            }
    return body
