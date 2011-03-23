package eu.venusc.cdmi;

import java.io.File;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import org.apache.http.auth.Credentials;
import org.apache.http.auth.UsernamePasswordCredentials;


public class CDMIClient {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		try{
		String remoteFNM = "hello.txt";
		URL endpoint = new URL("http://localhost:2364/");
		String localfile = "/home/venus/venus-c/vcdm/src/sdk/java/src/hello.txt";
		Map map = new HashMap();
		map.put("mimetype", "multipart/alternative");
		Credentials creds = new UsernamePasswordCredentials("username", "password");
		
		
		CDMIBlobOperations cd = new CDMIBlobOperations(creds, endpoint);

		cd.delete(remoteFNM);
		cd.create(localfile, remoteFNM, map);
		cd.update(localfile, remoteFNM, map);

		File f = cd.readFile(remoteFNM);

			for (String s: cd.getChildren("mydata")) {
				System.out.println(s);
			}
	
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}