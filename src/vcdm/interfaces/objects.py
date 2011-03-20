""" Data transfer objects for CDMI/cloud storage objects"""

class CDMIObject():
    uid = None
    metadata = None
    parent_container = None

class Blob(CDMIObject):
    fullpath = None   
    mimetype = None 
    
    def __init__(self, uid, parent_container, fullpath, mimetype = None, metadata = None):
        self.uid = uid
        self.parent_container = parent_container
        self.fullpath = fullpath
        self.mimetype = mimetype
        self.metadata = metadata
        

class Container(CDMIObject):
    children = None
    
    def __init__(self, uid, children = None):
        self.uid = uid
        self.children = children

class MessageQueue(CDMIObject):
    pass

class Domain(CDMIObject):
    pass