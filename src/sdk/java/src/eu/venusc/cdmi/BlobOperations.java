package eu.venusc.cdmi;
import java.util.List;

public interface BlobOperations  {
 
	// Create
	public void create(String localFile, String remoteFNM) throws Exception;
	
	public void delete(String remoteFNM) throws Exception;

	public void update(String localFile, String remoteFNM) throws Exception;
	
	public int readFile(String remoteFNM) throws Exception;

	public List<Blob> list(String remoteContainer);
	
}
