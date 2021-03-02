using System.Collections.Generic;

namespace ConsoleExtended
{
	public delegate void TreeVisitor<T>(T NodeData);

	/// <summary>
	/// Handles tree menu node structure.
	/// </summary>
	/// <typeparam name="T">Generic type</typeparam>
	public class CNode<T>
	{
		private T m_data;
		private LinkedList<CNode<T>> m_children;

		/// <summary>
		/// Constructor:
		/// </summary>
		/// <param name="data">The generic data object</param>
		public CNode(T data)
		{
			m_data		= data;
			m_children	= new LinkedList<CNode<T>>();
		}

		/// <summary>
		/// Add child to the node
		/// </summary>
		/// <param name="data">The child data</param>
		public void AddChild(T data)
		{
			m_children.AddFirst(new CNode<T>(data));
		}

		/// <summary>
		/// Add multiple children to the node
		/// </summary>
		/// <param name="datalist">List of generic types</param>
		public void AddChildren(List<T> datalist)
		{
			foreach(T data in datalist)
			{
				AddChild(data);
			}
		}

		/// <summary>
		/// Add multiple children to the node
		/// </summary>
		/// <param name="datalist">Array of generic types</param>
		public void AddChildren(T[] datalist)
		{
			foreach(T data in datalist)
			{
				AddChild(data);
			}
		}

		/// <summary>
		/// Get node's child from index
		/// </summary>
		/// <param name="i">The index</param>
		/// <returns>The child node</returns>
		public CNode<T> GetChild(int i)
		{
			foreach(CNode<T> n in m_children)
			{
				if(i-- == 0)
					return n;
			}

			return null;
		}

		/// <summary>
		/// Get node's children as CNode objects
		/// </summary>
		/// <returns>List of nodes</returns>
		public List<CNode<T>> GetChildren()
		{
			List<CNode<T>> children = new List<CNode<T>>(m_children);
			return children;
		}

		/// <summary>
		/// Return the list of all children node's data 
		/// </summary>
		/// <returns>List of generic types</returns>
		public List<T> GetChildDatalist()
		{
			List<T> dataList = new List<T>();

			foreach(CNode<T> child in m_children)
			{
				dataList.Add(child.m_data);
			}
			return dataList;
		}

		/// <summary>
		/// Check if the node has any children
		/// </summary>
		/// <returns><c>true</c> if node has at least one child; otherwise false</returns>
		public bool HasChildren()
		{
			return m_children.Count > 0;
		}

		/// <summary>
		/// Traverse the 
		/// </summary>
		/// <param name="node"></param>
		/// <param name="visitor"></param>
		public void Traverse(CNode<T> node, TreeVisitor<T> visitor)
		{
			visitor(node.m_data);
			foreach(CNode<T> child in node.m_children)
			{
				Traverse(child, visitor);
			}
		}
	}

	/// <summary>
	/// Acts as the tree root, managing underlying nodes.
	/// Keeps track of the menu selections.
	/// </summary>
	/// <typeparam name="T">Generic type</typeparam>
	public class CTree<T>
	{
		private Stack<CNode<T>>	m_selections;
		private CNode<T>		m_root;

		/// <summary>
		/// Gets the current menu selection
		/// </summary>
		public CNode<T> CurrentSelection
		{
			get
			{
				return m_selections.Peek();
			}
		}

		/// <summary>
		/// Gets the root node
		/// </summary>
		public CNode<T> Root
		{
			get
			{
				return m_root;
			}
			set
			{
				m_root = value;
			}
		}

		/// <summary>
		/// Constructor
		/// </summary>
		public CTree()
		{
			m_selections	= new Stack<CNode<T>>();
			m_root			= new CNode<T>(default(T));

			NewSelection(m_root);
		}

		/// <summary>
		/// Add a new selection to the selection tracker
		/// </summary>
		/// <param name="sel">The new selection</param>
		public void NewSelection(CNode<T> sel)
		{
			m_selections.Push(sel);
		}
		
		/// <summary>
		/// Return previous selection node.
		/// This will remove current selection from the list
		/// </summary>
		/// <returns>Tree node object</returns>
		public CNode<T> PreviousSelection()
		{
			if(m_selections.Count == 1) // The first selection is the root - cannot delete that.
				return m_selections.Peek();

			m_selections.Pop();
			return m_selections.Peek();
		}
	}
}
