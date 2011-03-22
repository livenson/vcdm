package eu.venusc.cdmi;

public class CDMIOperationException extends Exception{

	private int responseCode;
	
	public CDMIOperationException(String message, int responseCode) {
		super(message);
		this.responseCode = responseCode;
	}

	public int getResponseCode() {
		return responseCode;
	}

	public void setResponseCode(int responseCode) {
		this.responseCode = responseCode;
	}
	
}
