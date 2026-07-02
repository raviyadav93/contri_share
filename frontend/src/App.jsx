import { useState, useEffect } from 'react'
import Layout from './components/Layout'
import Dashboard from './features/dashboard/Dashboard'
import GroupList from './features/groups/GroupList'
import './App.css'

function App() {
  const [activeView, setActiveView] = useState('dashboard')
  const [appStatus, setAppStatus] = useState('ready') // 'loading', 'ready', 'error'

  // useEffect(() => {
  //   const checkHealth = async () => {
  //     try {
  //       const response = await fetch('/api/v1/health')
  //       if (response.ok) {
  //         setAppStatus('ready')
  //       } else {
  //         setAppStatus('error')
  //       }
  //     } catch (error) {
  //       console.error('Health check failed:', error)
  //       setAppStatus('error')
  //     } finally {
  //       setAppStatus('ready');
  //     }
  //   }

  //   checkHealth()
  // }, [])

  if (appStatus === 'loading') {
    return (
      <Layout>
        <div className="app-container">
          <div className="loading-state">
            <h2>Loading...</h2>
            <p>Connecting to contri_share API</p>
          </div>
        </div>
      </Layout>
    )
  }

  if (appStatus === 'error') {
    return (
      <Layout>
        <div className="app-container">
          <div className="error-state">
            <h2>Connection Error</h2>
            <p>Unable to connect to the API. Please check your configuration.</p>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout activeView={activeView} setActiveView={setActiveView}>
      <div className="app-container">
        {activeView === 'dashboard' && <Dashboard />}
        {activeView === 'groups' && <GroupList />}
      </div>
    </Layout>
  )
}

export default App
