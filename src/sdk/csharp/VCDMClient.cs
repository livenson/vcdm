using System;
using System.Net;
using System.IO;
using System.Text;

namespace VCDM
{
	public class VCDMClient
	{
		public string Endpoint { get; set; }
		public ICredentials Credentials { get; set; }
		
		public VCDMClient (string endpoint, ICredentials credentials)
		{
			Endpoint = endpoint;
			Credentials = credentials;
		}
		
		public VCDMClient (string endpoint)
		{
			Endpoint = endpoint;
			Credentials = null;
		}
		
		public Stream OpenRead(string remoteFilePath)
		{
			var req = WebRequest.Create(new Uri(Endpoint + "/" + remoteFilePath));
			req.Credentials = Credentials;
			req.Method = "GET";
			var webresp = req.GetResponse();
			return webresp.GetResponseStream();
		}
		
		public void Write(string remoteFilePath, Stream data)
		{
			var req = WebRequest.Create(new Uri(Endpoint + "/" + remoteFilePath));
			req.Credentials = Credentials;
			req.Method = "PUT";
			
			using (var reqstream = req.GetRequestStream())
			{
				int numread = 0;
				var buf = new byte[256];
				while ((numread = data.Read(buf, 0, 256)) > 0)
				{
					reqstream.Write(buf, 0, numread);
				}
			}
			
			var webresp = req.GetResponse();
			// TODO: use webresp to get, whether the function resulted in success of failure
		}
		
		public void Delete(string remoteFilePath)
		{
			var req = WebRequest.Create(new Uri(Endpoint + "/" + remoteFilePath));
			req.Credentials = Credentials;
			req.Method = "DELETE";
			req.GetResponse();
		}
		
		public void Update(string filePath, Stream data)
		{
			Write(filePath, data);
		}
		
		/// <summary>
		/// Search for files matching <see cref="pattern"/> under 
		/// the <see name="path"/> directory.
		/// </summary>
		/// <param name="pattern">
		/// A <see cref="System.String"/>
		/// </param>
		/// <param name="path">
		/// A <see cref="System.String"/>
		/// </param>
		public void Find(string pattern, string remotePath)
		{
			
		}
		
		//public void Find(string user) {}
		
		public void Find(long filesize) 
		{
			
		}
		
	}
}

