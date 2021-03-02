using System;

namespace ConsoleExtended
{
	public class CConsoleEx
	{
		protected CConsoleState		m_state;
		protected int				m_nColumns;
		protected int				m_nSpacingPerLine;
		protected ConsoleColor		m_selectionColour;

		/// <summary>
		/// Default constructor:
		/// Set the console state to insert mode
		/// Set the menu type to list (1 column)
		/// Set the line spacing to 10
		/// Set the color to red
		/// </summary>
		public CConsoleEx()
		{
			m_state			  = new CConsoleState();
			m_nColumns		  = 1;
			m_nSpacingPerLine = 10;
			m_selectionColour = ConsoleColor.Red;
		}

		/// <summary>
		/// Constructor:
		/// Set the object values
		/// </summary>
		/// <param name="consoleState">The console state</param>
		/// <param name="menuMode">The menu mode</param>
		/// <param name="nColumns">Number of columns (at least 1)</param>
		/// <param name="nSpacingPerLine">Spacing per line (at least 5)</param>
		/// <param name="colour">The highlight colour</param>
		public CConsoleEx(CConsoleState.State consoleState, CConsoleState.Mode menuMode, int nColumns, int nSpacingPerLine, ConsoleColor colour)
		{
			m_state				= new CConsoleState(consoleState, menuMode);
			m_nColumns			= Math.Max(1, nColumns);
			m_nSpacingPerLine	= Math.Max(5, nSpacingPerLine);
			m_selectionColour	= colour;
		}

		/// <summary>
		/// Display either the insert or navigate menu, depending on the console state
		/// </summary>
		/// <param name="strMenuTitle">Helper heading text block displayed on top of the console.</param>
		/// <param name="options">String array representing the available options</param>
		/// <returns>Index of the selection array, or any other valid integer</returns>
		public int DisplayMenu(string strMenuTitle, params string[] options)
		{
			Console.Clear();
			int nSelection = 0;

			do
			{
				if(m_state.IsNavigateState())
				{
					nSelection = HandleNavigationMenu(strMenuTitle, true, options);
				}
				else
				{
					nSelection = HandleInsertMenu(strMenuTitle, options);
				}

			} while(!IsSelectionValid(nSelection, options.Length));

			return nSelection;
		}

		/// <summary>
		/// Validate selection
		/// </summary>
		/// <param name="nSelectionIndex">Selected item as an array index</param>
		/// <param name="nItemCount">Number of possible selections</param>
		/// <returns><c>True</c> if valid; otherwise <c>false</c></returns>
		protected bool IsSelectionValid(int nSelectionIndex, int nItemCount)
		{
			return (-1 <= nSelectionIndex && nSelectionIndex < nItemCount);
		}

		/// <summary>
		/// Selection handler in the 'navigate' state.
		/// </summary>
		/// <param name="strHeader">Header text that will appear at the top of the console; <c>nullable</c></param>
		/// <param name="bCanExit">Controls if the function can be escaped using an escape key</param>
		/// <param name="options">Array of strings representing the possible selections</param>
		/// <returns>Index of the selected item from the options parameter or -1 (if escaped)</returns>
		protected virtual int HandleNavigationMenu(string strHeader, bool bCanExit, params string[] options)
		{
			// Setup
			int nCurrentSelection = 0;
			int nLastSelection = 0;

			ConsoleKey key;
			Console.CursorVisible = false;

			// Print the selections
			Console.Clear();
			Console.WriteLine(strHeader);
			int nStartY = Console.CursorTop + 1;

			if(m_state.IsGridView())
				DrawGridMenu(nCurrentSelection, nStartY, options);

			else
				DrawListMenu(nCurrentSelection, nStartY, options);

			do
			{
				// Track the current selection
				if(nCurrentSelection != nLastSelection)
					UpdateMenu(nLastSelection, nCurrentSelection, options[nLastSelection], options[nCurrentSelection], nStartY);

				key = Console.ReadKey(true).Key;
				nLastSelection = nCurrentSelection;

				switch(key)
				{
					case ConsoleKey.LeftArrow:
						NavigateLeft(ref nCurrentSelection);
						break;

					case ConsoleKey.RightArrow:
						NavigateRight(ref nCurrentSelection, options.Length);
						break;

					case ConsoleKey.UpArrow:
						NavigateUp(ref nCurrentSelection);
						break;

					case ConsoleKey.DownArrow:
						NavigateDown(ref nCurrentSelection, options.Length);
						break;

					case ConsoleKey.Escape:
						if(bCanExit)
							return -1;
						break;

					default:
						break;
				}
			} while(key != ConsoleKey.Enter);

			Console.CursorVisible = true;
			return nCurrentSelection;
		}

		/// <summary>
		/// Selection handler in the 'insert' mode
		/// </summary>
		/// <param name="strHeader">Header text that will appear at the top of the console; <c>nullable</c></param>
		/// <param name="options">Array of strings representing the possible selections</param>
		/// <returns>Index of the selected item from the options parameter</returns>
		protected virtual int HandleInsertMenu(string strHeader, params string[] options)
		{
			int nSelection = -1;
			Console.CursorVisible = true;
			bool bIsValidSelection = false;

			// Print the selections
			Console.Clear();
			Console.WriteLine(strHeader);
			int nStartY = Console.CursorTop + 1;

			if(m_state.IsGridView())
				DrawGridMenu(nSelection, nStartY, options);

			else
				DrawListMenu(nSelection, nStartY, options);

			do
			{
				// Set the cursor to the bottom of the console
				Console.SetCursorPosition(0, Console.WindowTop + Console.WindowHeight - 2);
				Console.Write(">>> ");
				string strInput = Console.ReadLine();

				if(strInput.Length < 1) // Empty string input are invalid
					continue;

				else if(strInput.ToLower() == "exit")
					return -1;

				else
				{
					nSelection = Array.FindIndex(options, delegate (string s)
					{
						return s == strInput;
					});

					if(nSelection >= 0)
						bIsValidSelection = true;
				}


			} while(!bIsValidSelection);

			return nSelection;
		}

		/// <summary>
		/// Draw the list options in a grid layout.
		/// </summary>
		/// <param name="nCursorPosition">Current cursor position</param>
		/// <param name="nStartTop">Offset from the top of the window</param>
		/// <param name="itemList">List of items to be displayed</param>
		protected void DrawGridMenu(int nCursorPosition, int nStartTop, params string[] itemList)
		{
			for(int i = 0; i < itemList.Length; i++)
			{
				Console.SetCursorPosition((i % m_nColumns) * m_nSpacingPerLine, nStartTop + i / m_nColumns);
				if(i == nCursorPosition)
					Console.ForegroundColor = m_selectionColour;

				Console.WriteLine(itemList[i]);
				Console.ResetColor();
			}
		}

		/// <summary>
		/// Draw a list of options as a list
		/// </summary>
		/// <param name="nCursorPosition">Current cursor position</param>
		/// <param name="nStartTop">Offset from the top of the window</param>
		/// <param name="itemList">List of items to be displayed</param>
		protected void DrawListMenu(int nCursorPosition, int nStartTop, params string[] itemList)
		{
			for(int i = 0; i < itemList.Length; i++)
			{
				Console.SetCursorPosition(1, nStartTop + i);

				if(i == nCursorPosition)
					Console.ForegroundColor = m_selectionColour;

				Console.WriteLine(itemList[i]);
				Console.ResetColor();
			}
		}

		/// <summary>
		/// Update the printed list of menu items by re-colouring only the changed items on the list
		/// </summary>
		/// <param name="nPreviousSelection">Index of the previously highlighted item</param>
		/// <param name="nCurrentSelection">Index of the currently selected item</param>
		/// <param name="strPreviousOption">String value of the previously selected option</param>
		/// <param name="strCurrentOption">String value of the currently selected option</param>
		/// <param name="nStartY">Starting Y position (lines from top)</param>
		protected void UpdateMenu(int nPreviousSelection, int nCurrentSelection, string strPreviousOption, string strCurrentOption, int nStartY)
		{
			if(m_state.IsListView())
				Console.SetCursorPosition(1, nStartY + nCurrentSelection);

			else if(m_state.IsGridView())
				Console.SetCursorPosition((nCurrentSelection % m_nColumns) * m_nSpacingPerLine, nStartY + nCurrentSelection / m_nColumns);

			Console.ForegroundColor = m_selectionColour;
			Console.Write("{0}", strCurrentOption);

			if(m_state.IsListView())
				Console.SetCursorPosition(1, nStartY + nPreviousSelection);

			else if(m_state.IsGridView())
				Console.SetCursorPosition((nPreviousSelection % m_nColumns) * m_nSpacingPerLine, nStartY + nPreviousSelection / m_nColumns);

			Console.ResetColor();
			Console.Write("{0}", strPreviousOption);
		}

		/// <summary>
		/// Handle selection calculation when 'up' is selected
		/// </summary>
		/// <param name="nCurrentSelection">Reference to the current selection</param>
		protected virtual void NavigateUp(ref int nCurrentSelection)
		{
			if(m_state.IsGridView() && nCurrentSelection >= m_nColumns)
				nCurrentSelection -= m_nColumns;

			else if(m_state.IsListView() && nCurrentSelection >= 1)
				nCurrentSelection--;
		}

		/// <summary>
		/// Handle selection calculation when 'down' is selected
		/// </summary>
		/// <param name="nCurrentSelection">Reference to the current selection</param>
		/// <param name="nOptionCount">Number of items in the list</param>
		protected virtual void NavigateDown(ref int nCurrentSelection, int nOptionCount)
		{
			if(m_state.IsGridView() && nCurrentSelection + m_nColumns < nOptionCount)
				nCurrentSelection += m_nColumns;

			else if(m_state.IsListView() && nCurrentSelection + 1 < nOptionCount)
				nCurrentSelection++;
		}

		/// <summary>
		/// Handle selection calculation when 'left' is selected
		/// </summary>
		/// <param name="nCurrentSelection">Reference to the current selection</param>
		protected virtual void NavigateLeft(ref int nCurrentSelection)
		{
			if(m_state.IsGridView() && nCurrentSelection > 0 && nCurrentSelection % m_nColumns > 0)
				nCurrentSelection--;

			else if(m_state.IsListView() && nCurrentSelection > 0)
				nCurrentSelection--;
		}

		/// <summary>
		/// Handle selection calculation when 'right' is selected
		/// </summary>
		/// <param name="nCurrentSelection">Reference to the current selection</param>
		/// <param name="nOptionCount">Numbers of items in the list</param>
		protected virtual void NavigateRight(ref int nCurrentSelection, int nOptionCount)
		{
			if(m_state.IsGridView() && nCurrentSelection + 1 < nOptionCount && nCurrentSelection % m_nColumns < m_nColumns - 1)
				nCurrentSelection++;

			else if(m_state.IsListView() && nCurrentSelection + 1 < nOptionCount && nCurrentSelection < 0)
				nCurrentSelection++;
		}
	}
}
