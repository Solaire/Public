using ConsoleExtended;
using System;

namespace Snake
{
	class Program
	{
		static void Main(string[] args)
		{
			CConsoleEx consoleEx = new CConsoleEx(CConsoleState.State.cState_Navigate, CConsoleState.Mode.cMode_ListView, 1, 5, ConsoleColor.Red);
			/*
			CMenuTree root = new CMenuTree(0, "root");
			root.InsertManyNodes(new string[]{ "level2A", "level2B" });

			int nSel = consoleEx.DisplayMenu("title", root.RetreiveChildrenStrings());
			for(;;)
			{
				nSel = consoleEx.DisplayMenu("title", root.GetChildByIndex(nSel).RetreiveChildrenStrings());
			}
			*/

			CTree<string> tree = new CTree<string>();
			tree.Root.AddChildren(new string[] { "level2A", "level2B" });
		}
	}
}
