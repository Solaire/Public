using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;

namespace XKDC_downloader
{
	/// <summary>
	/// Interaction logic for MainWindow.xaml
	/// </summary>
	public partial class MainWindow : Window
	{
		private CXKCD m_xkcd;
		private const string SAVE_PATH = @"./comics/";

		public MainWindow()
		{
			InitializeComponent();
			m_xkcd = new CXKCD();
			imgComic.Source = new BitmapImage(new Uri(m_xkcd.DownloadComic(m_xkcd.CurrentComicID)));
		}

		public void OnSaveAll(object sender, EventArgs e)
		{
			m_xkcd.DownloadAndSaveAllComics(SAVE_PATH);
		}

		public void OnPrevious(object sender, EventArgs e)
		{
			imgComic.Source = new BitmapImage(new Uri(m_xkcd.PreviousComic()));
		}

		public void OnNext(object sender, EventArgs e)
		{
			imgComic.Source = new BitmapImage(new Uri(m_xkcd.NextComic()));
		}

		public void OnSaveOne(object sender, EventArgs e)
		{
			m_xkcd.DownloadAndSaveCurrentComic(SAVE_PATH);
		}
	}
}
