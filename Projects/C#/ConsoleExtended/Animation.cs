using System;
using System.Threading;

namespace ConsoleExtended
{
	/// <summary>
	/// Handles text animations such as spinners and 
	/// </summary>
	public class CAnimation : IDisposable
	{
		private readonly string[]	m_sequence;
		private readonly int		m_nLeft;
		private readonly int		m_nTop;
		private readonly int		m_nDelay;

		private string				m_strCleaner;
		private int					m_nCounter;
		private bool				m_bActive;
		private readonly Thread		m_thread;

		public CAnimation(string[] sequence, int nLeft, int nTop, int nDelay = 100)
		{
			m_sequence   = sequence;
			m_nLeft		 = nLeft;
			m_nTop		 = nTop;
			m_nDelay	 = nDelay;
			MakeCleaningString();

			m_thread	= new Thread(Animate);
		}

		public void Start()
		{
			m_bActive = true;
			if(!m_thread.IsAlive)
				m_thread.Start();
		}

		public void Stop()
		{
			m_bActive = false;
			Draw(m_strCleaner);
		}

		private void Animate()
		{
			while(m_bActive)
			{
				DrawNext();
				Thread.Sleep(m_nDelay);
			}
		}

		private void Draw(string s)
		{
			Console.SetCursorPosition(m_nLeft, m_nTop);
			Console.Write(s);
		}

		private void DrawNext()
		{
			Draw(m_strCleaner);
			Draw(m_sequence[++m_nCounter % m_sequence.Length]);
		}

		public void Dispose()
		{
			Stop();
		}

		private void MakeCleaningString()
		{
			int nCharCount = 0;
			
			foreach(string s in m_sequence)
			{
				nCharCount = Math.Max(nCharCount, s.Length);
			}

			m_strCleaner = "";
			for(int i = 0; i < nCharCount; i++)
			{
				m_strCleaner += " ";
			}
		}
	}
}
