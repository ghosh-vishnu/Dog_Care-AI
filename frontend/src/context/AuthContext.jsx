import { createContext, useContext, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(localStorage.getItem('access_token'))
  const navigate = useNavigate()

  useEffect(() => {
    // Check if user is logged in on mount
    const storedToken = localStorage.getItem('access_token')
    if (storedToken) {
      setToken(storedToken)
      fetchUserProfile()
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUserProfile = async () => {
    try {
      const response = await api.get('/api/auth/users/me/')
      setUser(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching user profile:', error)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      setToken(null)
      setUser(null)
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      const response = await api.post('/api/auth/login/', {
        email,
        password,
      })
      
      const { tokens, user: userData } = response.data
      
      localStorage.setItem('access_token', tokens.access)
      localStorage.setItem('refresh_token', tokens.refresh)
      setToken(tokens.access)
      setUser(userData)
      
      return { success: true, data: response.data }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || { message: 'Login failed' },
      }
    }
  }

  const signup = async (userData) => {
    try {
      const response = await api.post('/api/auth/register/', userData)
      
      const { tokens, user: newUser } = response.data
      
      localStorage.setItem('access_token', tokens.access)
      localStorage.setItem('refresh_token', tokens.refresh)
      setToken(tokens.access)
      setUser(newUser)
      
      return { success: true, data: response.data }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || { message: 'Registration failed' },
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setToken(null)
    setUser(null)
    navigate('/login')
  }

  const value = {
    user,
    token,
    loading,
    login,
    signup,
    logout,
    isAuthenticated: !!token,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}



