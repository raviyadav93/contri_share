import { useState } from 'react'

function Dashboard() {
  const [stats] = useState({
    totalGroups: 0,
    totalExpenses: 0,
    youOwe: 0,
    youAreOwed: 0
  })

  return (
    <div className="dashboard-container">
      <h2>Dashboard</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Groups</h3>
          <p className="stat-value">{stats.totalGroups}</p>
        </div>
        
        <div className="stat-card">
          <h3>Total Expenses</h3>
          <p className="stat-value">{stats.totalExpenses}</p>
        </div>
        
        <div className="stat-card">
          <h3>You Owe</h3>
          <p className="stat-value negative">${stats.youOwe.toFixed(2)}</p>
        </div>
        
        <div className="stat-card">
          <h3>You Are Owed</h3>
          <p className="stat-value positive">${stats.youAreOwed.toFixed(2)}</p>
        </div>
      </div>

      <section className="dashboard-section">
        <h3>Recent Activity</h3>
        <div className="empty-state">
          <p>No recent activity yet. Start by creating a group or adding an expense.</p>
        </div>
      </section>
    </div>
  )
}

export default Dashboard
