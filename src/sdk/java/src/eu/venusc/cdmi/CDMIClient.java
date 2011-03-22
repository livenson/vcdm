package eu.venusc.cdmi;

import java.io.File;
import java.util.HashMap;
import java.util.Map;


public class CDMIClient {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String remoteFNM = "http://localhost:2364/hello.txt";
		String localfile = "/home/venus/venus-c/vcdm/src/sdk/java/src/hello.txt";
		Map map = new HashMap();
		
		CDMIBlobOperations cd = new CDMIBlobOperations();

		
		try {
			cd.delete(remoteFNM);
			cd.create(localfile, remoteFNM, map);
			cd.update(localfile, remoteFNM, map);
			File f = cd.readFile(remoteFNM);
			
			
			for (String s: cd.getChildren("http://localhost:2364/mydata")) {
				System.out.println(s);
			}
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}