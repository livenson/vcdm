package eu.venusc.cdmi;

class CommonBodyElements {

	String objectURI;
	String objectID;
	String parentURI;
	String domainURI;
	String mimetype;
	MetadataField metadata;
	
	public CommonBodyElements() {
	}
}

class BlobCreateRequest extends CommonBodyElements{

	String deserialize;
	String serialize;
	String copy;
	String move;
	String reference;
	String value;

	public BlobCreateRequest() {

	}
}

class BlobCreateResponse extends CommonBodyElements {

	String capabilitiesURI;
	String completionStatus;
	String percentComplete;
	
	public BlobCreateResponse() {

	}
}

class BlobReadResponse extends CommonBodyElements {

	String capabilitiesURI;
	String completionStatus;
	String percentComplete;
	String valuerange;
	String value;

	public BlobReadResponse() {

	}

}

class BlobUpdateRequest extends CommonBodyElements{
	
	String value;

	public BlobUpdateRequest() {

	}
}

class ContainerReadRequest extends CommonBodyElements {

	String capabilitiesURI;
	String completionStatus;
	String percentComplete;
	String exports;
	String snapshots;
	String childrenrange;
	String[] children;

	public ContainerReadRequest() {
	}
}

class MetadataField {
	
	int cdmi_size;
	String cdmi_mtime;
	String cdmi_atime;
	String cdmi_ctime;

	public MetadataField() {
	}
}

