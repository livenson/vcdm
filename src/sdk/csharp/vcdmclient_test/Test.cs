using System;
using NUnit.Framework;
using VCDM;
using System.Net;
using System.IO;
using System.Text;

namespace vcdmclient_test
{
	[TestFixture()]
	public class VCDMClientTest
	{
		[Test()]
		public void TestReadWrite()
		{
			var client = new VCDM.VCDMClient("http://localhost:8080/blob/",
			                                 new NetworkCredential("aaa", "aaa"));
			
			StringBuilder sb = new StringBuilder();
			sb.Append("Something to test for");
			
			byte[] buf = Encoding.UTF8.GetBytes(sb.ToString());
			using (MemoryStream ms = new MemoryStream(buf, false))
			{
				client.Write("/test1.txt", ms);
			}
			
			byte[] readbuf = new byte[256];
			Stream s = client.OpenRead("/test1.txt");
			StringBuilder resultString = new StringBuilder();
			
			int numread = 0;
			while ((numread = s.Read(readbuf, 0, readbuf.Length)) > 0)
			{
				resultString.Append(Encoding.UTF8.GetString(readbuf, 0, numread));
			}
			
			Assert.AreEqual(sb.ToString(), resultString.ToString());
			client.Delete("/test1.txt");
			
			try 
			{
				s = client.OpenRead("/test1.txt");
				Assert.Fail(); // must fail on OpenRead
			}
			catch (WebException)
			{
				// Must come here
			}
			
		}
		
		[Test()]
		public void TestUpdate()
		{
			var client = new VCDM.VCDMClient("http://localhost:8080/blob/", 
			                                 new NetworkCredential("aaa", "aaa"));
			
			var sb = new StringBuilder();
			sb.Append("#### Something to test for #1");
			
			using (MemoryStream ms = new MemoryStream(Encoding.UTF8.GetBytes(sb.ToString())))
			{
				client.Write("/test2", ms);
			}
			
			sb.Append("#### Something worth testing for #2");
			
			using (MemoryStream ms = new MemoryStream(Encoding.UTF8.GetBytes(sb.ToString())))
			{
				client.Update("/test2", ms);
			}
			
			var readbuf = new byte[256];
			var s = client.OpenRead("/test2");
			var resultString = new StringBuilder();
			
			int numread = 0;
			while ((numread = s.Read(readbuf, 0, readbuf.Length)) > 0)
			{
				var readstr = Encoding.UTF8.GetString(readbuf, 0, numread);
				resultString.Append(readstr);
			}
			
			Assert.AreEqual(sb.ToString(), resultString.ToString());
			client.Delete("/test2");
		}
	}
}

