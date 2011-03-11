"""
Abstract model of the Blob. This class should be seen as an Interface. 

TODO: At the moment we'd like to limit the number of dependencies. A more reliable
way would be to implement interfaces using Zope.Interfaces (extra-dependency) or
Python ABS (Python 2.6+).
"""
from errors import InternalError

class IBlob():
    
    backend_type = 'unknown'
    
    def create(self, fnm, content, metadata):
        """Create a new blob"""
        raise InternalError("Not implemented.")
    
    def read(self, fnm, range=None):
        """Retrieve a blob."""
        raise InternalError("Not implemented.")
    
    def update(self, fnm, content, metadata):
        """ Update blob with a new content and metadata."""
        raise InternalError("Not implemented.")
    
    def delete(self, fnm):
        """ Delete a specified blob."""
        raise InternalError("Not implemented.")
            