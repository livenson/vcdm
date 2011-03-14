package eu.venusc.cdmi;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;

public class Utils {


	 /**
	  * Fetch the entire contents of a text file, and return it in a String.
	  * This style of implementation does not throw Exceptions to the caller.
	  * As shown in: http://www.javapractices.com/topic/TopicAction.do?Id=42
	  * @param aFile is a file which already exists and can be read.
	  */
	  static public String getContents(File aFile) {
	    //...checks on aFile are elided
	    StringBuilder contents = new StringBuilder();
	    
	    try {
	      //use buffering, reading one line at a time
	      //FileReader always assumes default encoding is OK!
	     BufferedReader input =  new BufferedReader(new FileReader(aFile));
	     
	      try {
	        String line = null;

	        while (( line = input.readLine()) != null){
	          contents.append(line);
	          // TO BE FIXED THE LINE SEPERATOR!!!!!
	          //contents.append(System.getProperty("line.separator"));
	        }
	      }
	      finally {
	        input.close();
	      }
	    }
	    catch (IOException ex){
	      ex.printStackTrace();
	    }
	    
	    return contents.toString();
	  }

	  
	
}
