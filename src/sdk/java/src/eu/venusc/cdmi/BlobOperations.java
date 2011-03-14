package eu.venusc.cdmi;
import java.io.File;
import java.io.OutputStream;
import java.util.List;

public interface BlobOperations  {
 
	// Create
	public void create(String localFile, String remoteFNM) throws Exception;
	
	public void delete(String remoteFNM) throws Exception;
	public void update(String localFile, String remoteFNM) throws Exception;
	
	public int readFile(String remoteFNM) throws Exception;

	public List<Blob> list(String remoteContainer);

	/*
	public void create(byte[] content, URI remoteFNM);
	public void create(String content, URI remoteFNM);

	// Read
	public OutputStream read(URI remoteFNM);
	*/
	
}
