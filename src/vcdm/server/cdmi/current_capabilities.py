system = {
        
        "domains": False,
        "notification": False,
        "query": False,
        "queues": False,
            
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
        "list_children": True,
        "list_children_range": False,
        "read_metadata": True,
        "modify_metadata": True,
        "snapshot": False,
        "create_dataobject": True,
        "post_dataobject": False, 
        "create_container": True,
        "delete_container": True,
        "move_container": False,
        "copy_container": False,
    }
