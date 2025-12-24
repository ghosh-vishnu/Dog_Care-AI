import { useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import './Dashboard.css'

const Dashboard = () => {
  const { user, logout } = useAuth()

  useEffect(() => {
    // Fetch user data if needed
  }, [])

  return (
    <div className="dashboard-container">
      <div className="dashboard-card">
        <div className="dashboard-header">
          <h1>Welcome to Pet Health Dashboard</h1>
          <button onClick={logout} className="logout-button">
            Logout
          </button>
        </div>

        {user && (
          <div className="user-info">
            <div className="info-section">
              <h2>User Information</h2>
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Name:</span>
                  <span className="info-value">
                    {user.full_name || `${user.first_name} ${user.last_name}`}
                  </span>
                </div>
                <div className="info-item">
                  <span className="info-label">Email:</span>
                  <span className="info-value">{user.email}</span>
                </div>
                {user.phone_number && (
                  <div className="info-item">
                    <span className="info-label">Phone:</span>
                    <span className="info-value">{user.phone_number}</span>
                  </div>
                )}
                <div className="info-item">
                  <span className="info-label">Role:</span>
                  <span className="info-value">{user.role}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Veterinarian:</span>
                  <span className="info-value">
                    {user.is_veterinarian ? 'Yes' : 'No'}
                  </span>
                </div>
                <div className="info-item">
                  <span className="info-label">Member Since:</span>
                  <span className="info-value">
                    {new Date(user.date_joined).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="dashboard-content">
          <p>You are successfully logged in!</p>
          <p>This is your dashboard. You can add more features here.</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard


