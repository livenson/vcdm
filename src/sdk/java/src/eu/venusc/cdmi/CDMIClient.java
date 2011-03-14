package eu.venusc.cdmi;

import java.io.File;

public class CDMIClient {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String remoteFNM = "http://localhost:2364/hello.txt";
		String localfile = "/home/venus/venus-c/vcdm/src/sdk/java/bin/hello.txt";
		
		CDMIBlobOperations cd = new CDMIBlobOperations();
		try {
			//cd.create(localfile, remoteFNM);
			//cd.delete(remoteFNM);
			//cd.update(localfile, remoteFNM);
			int a = cd.readFile(remoteFNM);
			 
			 
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		

	}

}
;