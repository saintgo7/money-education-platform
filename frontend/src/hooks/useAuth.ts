import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { authApi } from '@/lib/api'

export function useAuth() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token')

    if (!token) {
      setLoading(false)
      return
    }

    try {
      const response = await authApi.me()
      setUser(response.data)
      localStorage.setItem('user_data', JSON.stringify(response.data))
    } catch (error) {
      console.error('Auth check failed:', error)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_data')
    } finally {
      setLoading(false)
    }
  }

  const login = async (credentials: { username: string; password: string }) => {
    const response = await authApi.login(credentials)
    const { access, refresh } = response.data

    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)

    await checkAuth()
    return response.data
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_data')
    setUser(null)
    router.push('/')
  }

  const isAuthenticated = !!user

  return {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    checkAuth,
  }
}
