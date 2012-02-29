system = {

        "cdmi_domains": False,
        "cdmi_notification": False,
        "cdmi_query": False,
        "cdmi_queues": False,

        # export protocols
        "cdmi_export_webdav": False,
        "cdmi_export_cifs": False,

        "cdmi_security_https_transport": True,

        # Storage System Metadata Capabilities
        "cdmi_size": True,
        "cdmi_ctime": True,
        "cdmi_atime": True,
        "cdmi_mtime": True,
        "cdmi_hash": False,
        "cdmi_acl": True,
    }

dataobject = {

        "cdmi_read_value": True,
        "cdmi_read_value_range": False,
        "cdmi_read_metadata": True,
        "cdmi_modify_value": True,
        "cdmi_modify_value_range": False,
        "cdmi_modify_metadata": True,
        "cdmi_delete_dataobject": True,
        "cdmi_serialize_dataobject": False,
        "cdmi_deserialize_dataobject": False,
    }

mq = {

        "cdmi_read_value": True,
        "cdmi_read_metadata": True,
        "cdmi_modify_value": True,
        "cdmi_modify_metadata": True,
        "cdmi_delete_queue": True,
    }

container = {
        "cdmi_list_children": True,
        "cdmi_list_children_range": False,
        "cdmi_read_metadata": True,
        "cdmi_modify_metadata": True,
        "cdmi_snapshot": False,
        "cdmi_create_dataobject": True,
        "cdmi_post_dataobject": False,
        "cdmi_create_container": True,
        "cdmi_delete_container": True,
        "cdmi_move_container": False,
        "cdmi_copy_container": False,
    }
