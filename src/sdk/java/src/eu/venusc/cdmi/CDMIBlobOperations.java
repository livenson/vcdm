package eu.venusc.cdmi;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URL;
import java.util.List;

import org.apache.http.Header;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import com.google.gson.Gson;
import com.google.gson.stream.JsonToken;

public class CDMIBlobOperations implements BlobOperations {

	@Override
	public void create(String localFNM, String remoteFNM) throws Exception {

		HttpClient httpclient = new DefaultHttpClient();

		try {
			// Create the request
			HttpResponse response = null;

			HttpPut httpput = new HttpPut(remoteFNM);
			httpput.setHeader("Content-Type",
					"application/vnd.org.snia.cdmi.dataobject+json");
			httpput.setHeader("Accept",
					"application/vnd.org.snia.cdmi.dataobject+json");
			httpput.setHeader("X-CDMI-Specification-Version", "1.0");

			String respStr = "{\n";
			respStr = respStr + "\"mimetype\" : \"" + "text/plain" + "\",\n";
			// TODO: encode content of the file into json using some library
			respStr = respStr + "\"value\" : \""
					+ Utils.getContents(new File(localFNM)) + "\"\n";
			respStr = respStr + "}\n";
			System.out.println(respStr);
			StringEntity entity = new StringEntity(respStr);
			httpput.setEntity(entity);

			response = httpclient.execute(httpput);

		} catch (Exception ex) {
			System.err.println(ex);
		}// exception
	}

	@Override
	public void update(String localFNM, String remoteFNM) throws Exception {

		HttpClient httpclient = new DefaultHttpClient();
		try {
			// Create the request
			HttpResponse response = null;
			HttpPut httpput = new HttpPut(remoteFNM);
			httpput.setHeader("Content-Type",
					"application/vnd.org.snia.cdmi.dataobject+json");
			httpput.setHeader("Accept",
					"application/vnd.org.snia.cdmi.dataobject+json");
			httpput.setHeader("X-CDMI-Specification-Version", "1.0");
			String respStr = "{\n";
			respStr = respStr + "\"mimetype\" : \"" + "text/plain" + "\",\n";
			respStr = respStr + "\"value\" : \""
					+ Utils.getContents(new File(localFNM)) + "\"\n";
			respStr = respStr + "}\n";
			System.out.println(respStr);
			StringEntity entity = new StringEntity(respStr);
			httpput.setEntity(entity);
			response = httpclient.execute(httpput);

		} catch (Exception ex) {
			System.out.println(ex);
		}
	}

	@Override
	public void delete(String remoteFNM) throws Exception {
		HttpClient httpclient = new DefaultHttpClient();
		try {
			// Create the request
			HttpResponse response = null;
			HttpDelete httpdelete = new HttpDelete(remoteFNM);
			httpdelete.setHeader("Content-Type",
					"application/vnd.org.snia.cdmi.container+json");
			httpdelete.setHeader("Accept",
					"application/vnd.org.snia.cdmi.dataobject+json");
			httpdelete.setHeader("X-CDMI-Specification-Version", "1.0");

			response = httpclient.execute(httpdelete);

		} catch (Exception ex) {
			System.err.println(ex);

		}

	}

	@Override
	public int readFile(String remoteFNM) throws Exception {

		File file = null;
		BufferedWriter bw = null;
		HttpClient httpclient = new DefaultHttpClient();

		try {
			HttpResponse response = null;
			HttpGet httpget = new HttpGet(remoteFNM);

			httpget.setHeader("Content-Type",
					"application/vnd.org.snia.cdmi.container+json");
			httpget.setHeader("Accept",
					"application/vnd.org.snia.cdmi.dataobject+json");

			httpget.setHeader("X-CDMI-Specification-Version", "1.0");

			response = httpclient.execute(httpget);

			Header[] hdr = response.getAllHeaders();
			System.out.println("Headers : " + hdr.length);
			for (int i = 0; i < hdr.length; i++) {
				System.out.println(hdr[i]);
			}

			Gson gson = new Gson();
			String content = gson.fromJson("\"value\"", String.class);

			URL url = new URL(remoteFNM);

			file = new File(System.getProperty("user.home") + url.getFile());
			bw = new BufferedWriter(new FileWriter(file));

			bw.write(content);
			bw.close();
			System.out.println("Your file has been written");

		} catch (IOException io) {
			io.printStackTrace();
		}
		return 0;

	}

	@Override
	public List<Blob> list(String remoteContainer) {
		// TODO Auto-generated method stub
		return null;
	}

}
