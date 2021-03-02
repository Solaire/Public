using System;
using System.Collections.Generic;
using System.Net;
using System.Text;
using System.Windows.Controls;
using System.IO;
using System.Windows.Media.Imaging;
using Newtonsoft.Json;

namespace XKDC_downloader
{
	public class CXKCD
	{
		private const string XKCD_URL			= @"https://xkcd.com/";
		private const string XKCD_IMG_URL		= @"https://imgs.xkcd.com/comics/";

		private uint m_nCurrentComicID;

		public uint CurrentComicID
		{
			get
			{
				return m_nCurrentComicID;
			}
			set
			{
				m_nCurrentComicID = value;
			}
		}

		public CXKCD()
		{
			m_nCurrentComicID	= GetLastestComicID();
		}

		public string DownloadComic(uint comicID)
		{
			using(WebClient client = new WebClient())
			{
				string json			= client.DownloadString(XKCD_URL + comicID + "/info.0.json");
				comicJson comicJson = JsonConvert.DeserializeObject<comicJson>(json);
				return XKCD_IMG_URL + Path.GetFileName(comicJson.img);
			}
		}

		public bool DownloadAndSaveComic(uint comicID, string savePath)
		{
			using(WebClient client = new WebClient())
			{
				string json			= client.DownloadString(XKCD_URL + comicID + "/info.0.json");
				comicJson comicJson = JsonConvert.DeserializeObject<comicJson>(json);
				string filename		= Path.GetFileName(comicJson.img);

				if(!Directory.Exists(savePath))
				{
					Directory.CreateDirectory(savePath);
				}

				client.DownloadFile(XKCD_IMG_URL + filename, savePath + comicID + "-" + filename);
			}

			return true;
		}

		public bool DownloadAndSaveCurrentComic(string savePath)
		{
			using(WebClient client = new WebClient())
			{
				string json			= client.DownloadString(XKCD_URL + m_nCurrentComicID + "/info.0.json");
				comicJson comicJson = JsonConvert.DeserializeObject<comicJson>(json);
				string filename		= Path.GetFileName(comicJson.img);

				if(!Directory.Exists(savePath))
				{
					Directory.CreateDirectory(savePath);
				}

				client.DownloadFile(XKCD_IMG_URL + filename, savePath + m_nCurrentComicID + "-" + filename);
			}

			return true;
		}

		public bool DownloadAndSaveAllComics(string savePath)
		{
			for(uint i = 1; i <= GetLastestComicID(); i++)
			{
				if(!DownloadAndSaveComic(i, savePath))
				{
					return false;
				}
			}

			return true;
		}

		public string NextComic()
		{
			if(m_nCurrentComicID < GetLastestComicID())
			{
				m_nCurrentComicID++;
			}

			return DownloadComic(m_nCurrentComicID);
		}

		public string PreviousComic()
		{
			if(m_nCurrentComicID > 1)
			{
				m_nCurrentComicID--;
			}

			return DownloadComic(m_nCurrentComicID);
		}

		private uint GetLastestComicID()
		{
			HtmlAgilityPack.HtmlDocument	archivePage	= new HtmlAgilityPack.HtmlDocument();
			HtmlAgilityPack.HtmlWeb			web			= new HtmlAgilityPack.HtmlWeb();
			archivePage = web.Load(XKCD_URL + "archive/");
			HtmlAgilityPack.HtmlNodeCollection items = archivePage.DocumentNode.SelectNodes("//*[@id='middleContainer']/a");

			// Last comic ID = comic count
			return (uint)items.Count;
		}
		private class comicJson
		{
			/// <summary>
			/// Comic number
			/// </summary>
			public int num { get; set; }

			/// <summary>
			/// Safe title for the comic
			/// </summary>
			public String safe_title { get; set; }

			/// <summary>
			/// Alt text for the comic
			/// </summary>
			public String alt { get; set; }

			/// <summary>
			/// Image url for the comic
			/// </summary>
			public string img { get; set; }
		}
	}
}
