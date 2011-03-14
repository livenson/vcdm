"""
Abstract model of the Datastore. This class should be seen as an Interface. 

TODO: At the moment we'd like to limit the number of dependencies. A more reliable
way would be to implement interfaces using Zope.Interfaces (extra-dependency) or
Python ABS (Python 2.6+).
"""
from vcdm.errors import InternalError

class IDatastore():
    
    backend_type = 'unknown'
    
    def read(self, docid):
        """ Read document from the store """
        raise InternalError("Not implemented.")
    
    def write(self, data, docid=None):
        """ Create or update a document with a defined data. 
        If 'docid' is None - create a new document, otherwise try to fetch and update.
        """
        raise InternalError("Not implemented.")
    
    def exists(self, docid):
        """Return True if a defined document exists in a store."""
        raise InternalError("Not implemented.")
    
    def delete(self, docid):
        """Delete document from the store."""
        raise InternalError("Not implemented.")

    def find_uid(self, fnm):
        """Find document uid by a document name."""
        raise InternalError("Not implemented.")

    def get_total_stats(self):
        """Get total statistics for a items indexed by a datastore."""
        raise InternalError("Not implemented.")
