package eu.venusc.cdmi;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.InputStream;
import java.net.URI;
import java.net.URL;
import java.util.Map;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import com.google.gson.Gson;

public class CDMIBlobOperations {

	public CDMIBlobOperations() {
	}

	public int create(URI local, URI remote, Map parameters) throws Exception {

		HttpClient httpclient = new DefaultHttpClient();

		HttpResponse response = null;

		HttpPut httpput = new HttpPut(remote);

		httpput.setHeader("Content-Type", CDMIContentType.CDMI_DATA);
		httpput.setHeader("Accept", CDMIContentType.CDMI_DATA);
		httpput.setHeader("X-CDMI-Specification-Version", "1.0");

		String respStr = "{\n";
		respStr = respStr + "\"mimetype\" : \"" + "text/plain" + "\",\n";
		respStr = respStr + "\"value\" : \""
				+ Utils.getContents(new File(local.getPath())) + "\"\n";
		respStr = respStr + "}\n";

		StringEntity entity = new StringEntity(respStr);
		httpput.setEntity(entity);

		response = httpclient.execute(httpput);
		int responseCode = response.getStatusLine().getStatusCode();

		switch (responseCode) {

		case 201:
			/* New data object was created */
			break;

		case 400:
			throw new CDMIOperationException(
					"Invalid parameter of field names in the request: ",
					responseCode);
		case 401:
			throw new CDMIOperationException(
					"Incorrect or missing authentication credentials: ",
					responseCode);
		case 403:
			throw new CDMIOperationException(
					"Client lacks the proper authorization to perform this request: ",
					responseCode);

		case 409:
			throw new CDMIOperationException(
					"The operation conflicts with a non-CDMI access protocol lock, or could cause a state transition error on the server or he data object cannot be deleted.",
					responseCode);
		}
		return responseCode;

	}

	public int create(String localFNM, String remoteFNM, Map parameters)
			throws Exception {
		return create(new URI(localFNM), new URI(remoteFNM), parameters);
	}

	public int update(String localFNM, String remoteFNM, Map parameters)
			throws Exception {
		HttpClient httpclient = new DefaultHttpClient();
		HttpResponse response = null;
		HttpPut httpput = new HttpPut(remoteFNM);

		httpput.setHeader("Content-Type", CDMIContentType.CDMI_DATA);
		httpput.setHeader("Accept", CDMIContentType.CDMI_DATA);
		httpput.setHeader("X-CDMI-Specification-Version", "1.0");

		String respStr = "{\n";
		respStr = respStr + "\"mimetype\" : \"" + "text/plain" + "\",\n";

		respStr = respStr + "\"value\" : \""
				+ Utils.getContents(new File(localFNM)) + "\"\n";
		respStr = respStr + "}\n";

		StringEntity entity = new StringEntity(respStr);
		httpput.setEntity(entity);

		response = httpclient.execute(httpput);

		int responseCode = response.getStatusLine().getStatusCode();

		switch (responseCode) {

		case 200:
			/* New metadata and/or content accepted */
			break;
		case 302:
			throw new CDMIOperationException(
					"The URI is a reference to another URI: " + remoteFNM,
					responseCode);
		case 400:
			throw new CDMIOperationException(
					"Invalid parameter of field names in the request: "
							+ remoteFNM, responseCode);
		case 401:
			throw new CDMIOperationException(
					"Incorrect or missing authentication credentials: "
							+ remoteFNM, responseCode);
		case 403:
			throw new CDMIOperationException(
					"Client lacks the proper authorization to perform this request: "
							+ remoteFNM, responseCode);
		case 404:
			throw new CDMIOperationException(
					"An update was attempted on an object that does not exist: "
							+ remoteFNM, responseCode);
		case 409:
			throw new CDMIOperationException(
					"The operation conflicts with a non-CDMI access protocol lock, or could cause a state transition error on the server or he data object cannot be deleted."
							+ remoteFNM, responseCode);
		}

		return responseCode;
	}

	public void delete(String remoteFNM) throws Exception {
		HttpClient httpclient = new DefaultHttpClient();
		HttpDelete httpdelete = new HttpDelete(remoteFNM);
		httpdelete.setHeader("Content-Type", CDMIContentType.CDMI_DATA);
		httpdelete.setHeader("Accept", CDMIContentType.CDMI_DATA);
		httpdelete.setHeader("X-CDMI-Specification-Version", "1.0");

		HttpResponse response = httpclient.execute(httpdelete);

		int responseCode = response.getStatusLine().getStatusCode();

		switch (responseCode) {

		case 200:
			break;
		case 400:
			throw new CDMIOperationException(
					"Invalid parameter of field names in the request: "
							+ remoteFNM, responseCode);
		case 401:
			throw new CDMIOperationException(
					"Incorrect or missing authentication credentials: "
							+ remoteFNM, responseCode);
		case 403:
			throw new CDMIOperationException(
					"Client lacks the proper authorization to perform this request: "
							+ remoteFNM, responseCode);
		case 404:
			throw new CDMIOperationException(
					"The resource specified was not found: " + remoteFNM,
					responseCode);
		case 409:
			throw new CDMIOperationException(
					"The operation conflicts with a non-CDMI access protocol lock, or could cause a state transition error on the server or he data object cannot be deleted: "
							+ remoteFNM, responseCode);
		}
	}

	public File readFile(String remoteFNM) throws Exception {

		File file = null;
		BufferedWriter bw = null;
		HttpClient httpclient = new DefaultHttpClient();

		HttpGet httpget = new HttpGet(remoteFNM);

		httpget.setHeader("Accept", CDMIContentType.CDMI_DATA);
		httpget.setHeader("Content-Type", CDMIContentType.CDMI_OBJECT);
		httpget.setHeader("X-CDMI-Specification-Version", "1.0");

		HttpResponse response = httpclient.execute(httpget);

		int responseCode = response.getStatusLine().getStatusCode();

		switch (responseCode) {

		case 200:
			/* Valid response is enclosed */
			break;
		case 302:
			throw new CDMIOperationException(
					"The URI is a reference to another URI: " + remoteFNM,
					responseCode);
		case 400:
			throw new CDMIOperationException(
					"Invalid parameter of field names in the request: "
							+ remoteFNM, responseCode);
		case 401:
			throw new CDMIOperationException(
					"Incorrect or missing authentication credentials: "
							+ remoteFNM, responseCode);
		case 403:
			throw new CDMIOperationException(
					"Client lacks the proper authorization to perform this request: "
							+ remoteFNM, responseCode);
		case 404:
			throw new CDMIOperationException(
					"An update was attempted on an object that does not exist: "
							+ remoteFNM, responseCode);
		case 406:
			throw new CDMIOperationException(
					"The server is unable to provide the object in the content-type specified in the Accept header: "
							+ remoteFNM, responseCode);
		}

		InputStream respStream = response.getEntity().getContent();
		Gson gson = new Gson();
		BlobReadResponse responseBody = gson
				.fromJson(Utils.convertStreamToString(respStream),
						BlobReadResponse.class);


		if (responseBody.mimetype.equals("text/plain")) {
			URL url = new URL(remoteFNM);

			file = new File(System.getProperty("user.home") + url.getFile());
			bw = new BufferedWriter(new FileWriter(file));
			bw.write(responseBody.value);
			bw.close();
		}
		return file;
	}

	public String[] getChildren(String remoteContainer) throws Exception {

		HttpClient httpclient = new DefaultHttpClient();

		HttpResponse response = null;
		HttpGet httpget = new HttpGet(remoteContainer);
		httpget.setHeader("Content-Type", CDMIContentType.CDMI_CONTAINER);
		httpget.setHeader("Accept", CDMIContentType.CDMI_OBJECT);
		httpget.setHeader("X-CDMI-Specification-Version", "1.0");
		response = httpclient.execute(httpget);

		int responseCode = response.getStatusLine().getStatusCode();

		switch (responseCode) {

		case 200:
			/* Metadata for the container Object provided in the Message Body */
			break;
		case 302:
			throw new CDMIOperationException(
					"The URI is a reference to another URI: " + remoteContainer,
					responseCode);
		case 400:
			throw new CDMIOperationException(
					"Invalid parameter of field names in the request	: "
							+ remoteContainer, responseCode);
		case 401:
			throw new CDMIOperationException(
					"Incorrect or missing authentication credentials: "
							+ remoteContainer, responseCode);
		case 403:
			throw new CDMIOperationException(
					"Client lacks the proper authorization to perform this request: "
							+ remoteContainer, responseCode);
		case 404:
			throw new CDMIOperationException(
					"A container was not found at the specified URI: "
							+ remoteContainer, responseCode);
		case 406:
			throw new CDMIOperationException(
					"The server is unable to provide the object in the content-type specified in the Accept header: "
							+ remoteContainer, responseCode);
		}

		InputStream respStream = response.getEntity().getContent();
		Gson gson = new Gson();

		ContainerReadRequest responseBody = gson.fromJson(
				Utils.convertStreamToString(respStream),
				ContainerReadRequest.class);

		return responseBody.children;
	}

}


