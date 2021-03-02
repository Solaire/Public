using ConsoleExtended;
using System;
using System.Collections.Generic;

namespace ConsoleApp1
{
	class Program
	{
		static void Main(string[] args)
		{
			/*
			CTree<string> tree = new CTree<string>();
			tree.Root.AddChildren(new string[] { "1A", "1B", "1C" });
			List<CNode<string>> childlist1 = tree.Root.GetChildren();

			childlist1[0].AddChildren(new string[] { "2A", "2B", "2C" });
			childlist1[1].AddChildren(new string[] { "2D", "2E", "2G" });
			childlist1[2].AddChildren(new string[] { "2G", "2H", "2I" });

			CConsoleEx consoleEx = new CConsoleEx(CConsoleState.State.cState_Navigate, CConsoleState.Mode.cMode_ListView, 1, 5, ConsoleColor.Yellow);

			bool loop = true;

			while(loop)
			{
				int selection = consoleEx.DisplayMenu("title", tree.CurrentSelection.GetChildDatalist().ToArray());

				if(selection == -1)
				{
					tree.PreviousSelection();
					continue;
				}

				CNode<string> newSel = tree.CurrentSelection.GetChild(selection);
				if(newSel == null || !newSel.HasChildren())
				{
					loop = false;
					continue;
				}

				if(!Console.CapsLock)
					tree.NewSelection(newSel);
			}
			*/

			/*
			CAnimation animation = new CAnimation(new string[] { "8D", "8-D", "8--D", "8---D" }, 10, 10);

			animation.Start();

			System.Threading.Thread.Sleep(30000);

			animation.Stop();
			
			Console.ReadLine();
			*/
			while(true)
			{
				System.Threading.Thread.Sleep(1000);
				Console.Clear();
				Console.SetCursorPosition(10, 10);
				Console.Write("12345678");
				Console.SetCursorPosition(10, 11);
				Console.Write("12345678");
				Console.SetCursorPosition(10, 12);
				Console.Write("12345678");
				Console.SetCursorPosition(10, 14);
			}
		}
	}
}
