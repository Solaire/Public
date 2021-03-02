namespace ConsoleExtended
{
	/// <summary>
	/// Handles console attributes such as navigation mode and menu mode
	/// </summary>
	public sealed class CConsoleState
	{
		/// <summary>
		/// Buffer state enumerator
		/// </summary>
		public enum State
		{
			cState_Insert	= 1,
			cState_Navigate = 2,
		}

		/// <summary>
		/// Buffer mode enumerator
		/// </summary>
		public enum Mode
		{
			cMode_ListView = 1,
			cMode_GridView = 2,
		}

		private State m_state;
		private Mode m_mode;

		/// <summary>
		/// Constructor
		/// </summary>
		/// <param name="state">The console state; insert state is the default</param>
		/// <param name="mode">The menu mode; list view is the default value</param>
		public CConsoleState(State state = State.cState_Insert, Mode mode = Mode.cMode_ListView)
		{
			m_state = state;
			m_mode  = mode;
		}

		/// <summary>
		/// Check if the console state is set to insert state
		/// </summary>
		/// <returns><c>true</c> if insert state; otherwise <c>false</c></returns>
		public bool IsInsertState()
		{
			return m_state == State.cState_Insert;
		}

		/// <summary>
		/// Check if the console state is set to navigate state
		/// </summary>
		/// <returns><c>true</c> if navigate state; otherwise <c>false</c></returns>
		public bool IsNavigateState()
		{
			return m_state == State.cState_Navigate;
		}

		/// <summary>
		/// Check if the console mode is in the list view
		/// </summary>
		/// <returns><c>true</c> if list view; otherwise <c>false</c></returns>
		public bool IsListView()
		{
			return m_mode == Mode.cMode_ListView;
		}

		/// <summary>
		/// Check if the console mode is in the grid view
		/// </summary>
		/// <returns><c>true</c> if grid view; otherwise <c>false</c></returns>
		public bool IsGridView()
		{
			return m_mode == Mode.cMode_GridView;
		}

		/// <summary>
		/// Set the console state;
		/// </summary>
		/// <param name="newState">The new console state</param>
		public void SetState(State newState)
		{
			m_state = newState;
		}

		/// <summary>
		/// Set the menu mode
		/// </summary>
		/// <param name="newMode">The new menu mode</param>
		public void SetMode(Mode newMode)
		{
			m_mode = newMode;
		}
	}
}
