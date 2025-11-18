'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState, useEffect } from 'react'
import { Button } from './ui/Button'
import { BookOpen, User, LogOut, Settings, BarChart } from 'lucide-react'

export function Navbar() {
  const pathname = usePathname()
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userType, setUserType] = useState<string>('')

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token')
    setIsLoggedIn(!!token)

    // Get user type from stored user data (you'd get this from API)
    const userData = localStorage.getItem('user_data')
    if (userData) {
      try {
        const user = JSON.parse(userData)
        setUserType(user.user_type)
      } catch (e) {
        console.error('Failed to parse user data:', e)
      }
    }
  }, [pathname])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_data')
    setIsLoggedIn(false)
    window.location.href = '/'
  }

  if (!isLoggedIn) {
    return null // Header component handles logged out state
  }

  const navItems = userType === 'instructor' ? [
    { href: '/instructor/dashboard', label: '대시보드', icon: BarChart },
    { href: '/instructor/courses/new', label: '코스 만들기', icon: BookOpen },
  ] : [
    { href: '/dashboard', label: '대시보드', icon: BarChart },
    { href: '/courses', label: '코스', icon: BookOpen },
    { href: '/ai-tutor', label: 'AI 튜터', icon: User },
  ]

  return (
    <nav className="bg-white border-b">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center gap-2">
              <BookOpen className="w-6 h-6 text-primary" />
              <span className="font-bold">Money Education</span>
            </Link>

            <div className="hidden md:flex items-center gap-6">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center gap-2 hover:text-primary transition-colors ${
                      pathname === item.href ? 'text-primary' : 'text-gray-700'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    {item.label}
                  </Link>
                )
              })}
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Link href="/profile">
              <Button variant="ghost" size="sm">
                <User className="w-4 h-4 mr-2" />
                프로필
              </Button>
            </Link>
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              <LogOut className="w-4 h-4 mr-2" />
              로그아웃
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
