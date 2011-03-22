package eu.venusc.cdmi;

public class ContainerReadRequest extends CommonBodyElements{

	String capabilitiesURI;
	String completionStatus;
	String percentComplete;
    MetadataField metadata;
	String exports;
	String snapshots;
	String childrenrange;
	String[] children;

	public ContainerReadRequest() {
	}
}
