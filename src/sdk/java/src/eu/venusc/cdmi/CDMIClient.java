package eu.venusc.cdmi;


public class CDMIClient {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String remoteFNM = "http://localhost:2364/queue";
		String localfile = "";
		
		//CDMIBlobOperations cd = new CDMIBlobOperations();
		CDMIMQOperations mq = new CDMIMQOperations();
		
		
		try {
			//cd.create(localfile, remoteFNM);
			//cd.delete(remoteFNM);
			//cd.update(localfile, remoteFNM);
			//int a = cd.readFile(remoteFNM);
			mq.createQueueObj(remoteFNM);	

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		

	}

}
;