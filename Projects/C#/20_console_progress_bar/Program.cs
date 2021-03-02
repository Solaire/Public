using System;
using System.Threading;

namespace ConsoleProgress
{
    class Program
    {
        static void Main(string[] args)
        {

            Console.Write("Working. ");
            CProgressBar progress = new CProgressBar(10);

            progress.Start();

            for(int i = 0; i < 100; i++)
            {
                progress.Report((double)i / 100);
                Thread.Sleep(50);
            }

            progress.Stop();
            Console.WriteLine("Finished");
            Console.ReadLine();
        }
    }
}
