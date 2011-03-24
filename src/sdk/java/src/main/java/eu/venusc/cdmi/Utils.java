package eu.venusc.cdmi;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.StringWriter;
import java.io.Writer;

public class Utils {

	static public String getContents(File file) throws IOException{
		
		StringBuilder sb = new StringBuilder();
		try {
		    DataInputStream in = new DataInputStream(new FileInputStream(file));

		    BufferedReader br = new BufferedReader(new InputStreamReader(in, "UTF-8"));
		    String strLine;
		    
		    while ((strLine = br.readLine()) != null)
		        sb.append(strLine);
		      in.close();
		      }catch (IOException e){
		        e.printStackTrace();
		      }
		    return sb.toString();
		}

	
	public static String convertStreamToString(InputStream is)
			throws IOException {
		/*
		 * To convert the InputStream to String we use the Reader.read(char[]
		 * buffer) method. We iterate until the Reader return -1 which means
		 * there's no more data to read. We use the StringWriter class to
		 * produce the string.
		 */
		if (is != null) {
			Writer writer = new StringWriter();

			char[] buffer = new char[1024];
			try {
				Reader reader = new BufferedReader(new InputStreamReader(is));
				int n;
				while ((n = reader.read(buffer)) != -1) {
					writer.write(buffer, 0, n);
				}
			} finally {
				is.close();
			}
			return writer.toString();
		} else {
			return "";
		}
	}

}
