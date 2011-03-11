"""
Abstract model of the MessageQueue. This class should be seen as an Interface. 

TODO: At the moment we'd like to limit the number of dependencies. A more reliable
way would be to implement interfaces using Zope.Interfaces (extra-dependency) or
Python ABS (Python 2.6+).
"""
from errors import InternalError

class MessageQueue():
    def create(self, queuename):
        """Create queue with a specified name"""
        raise InternalError("Not implemented.")
    
    def delete(self, queuename):
        """Delete a specified queue"""
        raise InternalError("Not implemented.") 
    
    def enqueue(self, queuename, value):
        """Enqueue a new ''value'' into a specified queue"""
        raise InternalError("Not implemented.") 
    
    def get(self, queuename):
        """Get the last enqueued message from a queue"""
        raise InternalError("Not implemented.")
    
    def delete_message(self, quename):
        """Delete last value from a queue"""
        raise InternalError("Not implemented.")