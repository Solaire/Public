using System;
using System.Collections.Generic;
using System.Text;
using System.Threading;

namespace ConsoleProgress
{
    public class CProgressBar : IDisposable, IProgress<double>
    {
        private const string m_sequence = @"/-\|";
        private int m_counter;
        private int m_size;
        private double m_progress;
        private readonly int m_left;
        private readonly int m_top;
        private readonly int m_delay;
        private bool m_active;
        private readonly Thread m_thread;

        public CProgressBar(int left = 0, int top = 0, int size = 10, int delay = 200)
        {
            m_left     = left;
            m_top      = top;
            m_delay    = delay;
            m_size     = size;
            m_thread   = new Thread(Update);
            m_counter  = 0;
            m_progress = 0.0;
            m_active   = false;
        }

        public void Start()
        {
            m_active = true;
            if(!m_thread.IsAlive)
            {
                m_thread.Start();
            }
        }

        public void Stop()
        {
            m_active = false;
            Draw(new String(' ', Console.BufferWidth - m_left));
        }

        private void Update()
        {
            while(m_active)
            {
                DrawProgress();
                Thread.Sleep(m_delay);
            }
        }

        private void DrawProgress()
        {
            int percent         = (int)(m_progress * 100);
            int progressCount   = (int)(m_progress * m_size);
            string text         = string.Format("[{0}{1}] {2,3}% {3}", new string('#', progressCount), new string('-', m_size - progressCount), percent, m_sequence[++m_counter % m_sequence.Length]);

            Draw(text);
        }

        private void Draw<T>(T value, bool lineBreak = false)
        {
            Console.SetCursorPosition(m_left, m_top);
            Console.ForegroundColor = ConsoleColor.White;
            if(lineBreak)
            {
                Console.WriteLine(value);
            }
            else
            {
                Console.Write(value);
            }
        }

        public void Dispose()
        {
            Stop();
        }

        public void Report(double value)
        {
            value = Math.Max(0, Math.Min(1, value));
            Interlocked.Exchange(ref m_progress, value);
        }
    }
}

/*
using System;
using System.Text;
using System.Threading;

/// <summary>
/// An ASCII progress bar
/// </summary>
public class ProgressBar : IDisposable, IProgress<double> {
	private const int blockCount = 10;
	private readonly TimeSpan animationInterval = TimeSpan.FromSeconds(1.0 / 8);
	private const string animation = @"|/-\";

	private readonly Timer timer;

	private double currentProgress = 0;
	private string currentText = string.Empty;
	private bool disposed = false;
	private int animationIndex = 0;

	public ProgressBar() {
		timer = new Timer(TimerHandler);

		// A progress bar is only for temporary display in a console window.
		// If the console output is redirected to a file, draw nothing.
		// Otherwise, we'll end up with a lot of garbage in the target file.
		if (!Console.IsOutputRedirected) {
			ResetTimer();
		}
	}

	public void Report(double value) {
		// Make sure value is in [0..1] range
		value = Math.Max(0, Math.Min(1, value));
		Interlocked.Exchange(ref currentProgress, value);
	}

	private void TimerHandler(object state) {
		lock (timer) {
			if (disposed) return;

			int progressBlockCount = (int) (currentProgress * blockCount);
			int percent = (int) (currentProgress * 100);
			string text = string.Format("[{0}{1}] {2,3}% {3}",
				new string('#', progressBlockCount), new string('-', blockCount - progressBlockCount),
				percent,
				animation[animationIndex++ % animation.Length]);
			UpdateText(text);

			ResetTimer();
		}
	}

	private void UpdateText(string text) {
		// Get length of common portion
		int commonPrefixLength = 0;
		int commonLength = Math.Min(currentText.Length, text.Length);
		while (commonPrefixLength < commonLength && text[commonPrefixLength] == currentText[commonPrefixLength]) {
			commonPrefixLength++;
		}

		// Backtrack to the first differing character
		StringBuilder outputBuilder = new StringBuilder();
		outputBuilder.Append('\b', currentText.Length - commonPrefixLength);

		// Output new suffix
		outputBuilder.Append(text.Substring(commonPrefixLength));

		// If the new text is shorter than the old one: delete overlapping characters
		int overlapCount = currentText.Length - text.Length;
		if (overlapCount > 0) {
			outputBuilder.Append(' ', overlapCount);
			outputBuilder.Append('\b', overlapCount);
		}

		Console.Write(outputBuilder);
		currentText = text;
	}

	private void ResetTimer() {
		timer.Change(animationInterval, TimeSpan.FromMilliseconds(-1));
	}

	public void Dispose() {
		lock (timer) {
			disposed = true;
			UpdateText(string.Empty);
		}
	}

} 
*/