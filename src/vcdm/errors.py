class VCDMError(Exception):
    """Base class for VCDM Errors"""
    pass

class ProtocolError(VCDMError):
    """Raised when a certain front-end protocol is violated."""
    def __init__(self, msg):
        self.msg = msg
        
class InternalError(VCDMError):
    """Raised when a back-end operation fails."""
    def __init__(self, msg):
        self.msg = msg