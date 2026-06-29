import '../App.css'

function Layout({ children, activeView, setActiveView }) {
  return (
    <div className="app-wrapper">
      <nav className="navbar">
        <div className="navbar-brand">
          <h1>contri_share</h1>
        </div>
        <ul className="navbar-menu">
          <li>
            <button
              className={`nav-link ${activeView === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveView('dashboard')}
            >
              Dashboard
            </button>
          </li>
          <li>
            <button
              className={`nav-link ${activeView === 'groups' ? 'active' : ''}`}
              onClick={() => setActiveView('groups')}
            >
              Groups
            </button>
          </li>
        </ul>
      </nav>

      <main className="main-content">
        {children}
      </main>

      <footer className="app-footer">
        <p>&copy; 2024 contri_share. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default Layout
