system = {
        
        "domains": False,
        "notification": False,
        "query": False,
        "queues": True,
            
        # export protocols        
        "export_webdav": False,
        "export_cifs": False,

        "security_https_transport": True,        

        
        # Storage System Metadata Capabilities
        "size": True,
        "ctime": True,
        "atime": False,
        "mtime": False,
        "hash": False,
        "acl": False,
    }

dataobject = {

        "read_value": True,
        "read_value_range": False,
        "read_metadata": True,
        "modify_value": True,
        "modify_value_range": False,
        "modify_metadata": True,
        "delete_dataobject": True,
        "serialize_dataobject": False,
        "deserialize_dataobject": False,
    }

mq = {

        "read_value": True,        
        "read_metadata": True,
        "modify_value": True,
        "modify_metadata": True,
        "delete_queue": True,
    }

container = {
        "list_children": False,
        "list_children_range": False,
        "read_metadata": False,
        "modify_metadata": False,
        "snapshot": False,
        "create_dataobject": False,
        "post_dataobject": False, 
        "create_container": False,
        "delete_container": False,
        "move_container": False,
        "copy_container": False,
    }