package eu.venusc.cdmi;

import java.io.File;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;

public class CDMIMQOperations implements MQOperations {

	@Override
	public void createQueueObj(String queueName)
			throws Exception {

		HttpClient httpclient = new DefaultHttpClient();
		try {
			HttpResponse response = null;

			HttpPut httpput = new HttpPut(queueName);

			httpput.setHeader("Content-Type",
					"application/vnd.org.snia.cdmi.queue+json");
			httpput.setHeader("Accept",
					"application/vnd.org.snia.cdmi.queue+json");
			httpput.setHeader("X-CDMI-Specification-Version", "1.0");

			
			String respStr = "{\n";
			respStr = respStr + "      "+ "\"metadata\" : { \n"
					 + "\n      } \n";
			respStr = respStr + "}\n";

			StringEntity entity = new StringEntity(respStr);
			httpput.setEntity(entity);

			System.out.println(respStr);
			response = httpclient.execute(httpput);
		} catch (Exception e) {
			// TODO: handle exception
		}
	}
}
