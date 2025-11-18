'use client'

import Link from 'next/link'
import { useState } from 'react'
import { Button } from './ui/Button'
import { BookOpen, User, Menu, X } from 'lucide-react'

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <header className="border-b bg-white sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <BookOpen className="w-8 h-8 text-primary" />
            <span className="text-xl font-bold">Money Education</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/courses" className="hover:text-primary transition-colors">
              코스
            </Link>
            <Link href="/about" className="hover:text-primary transition-colors">
              소개
            </Link>
            <Link href="/pricing" className="hover:text-primary transition-colors">
              가격
            </Link>
          </nav>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center gap-4">
            <Link href="/auth/login">
              <Button variant="ghost">로그인</Button>
            </Link>
            <Link href="/auth/register">
              <Button>시작하기</Button>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X /> : <Menu />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t">
            <nav className="flex flex-col gap-4">
              <Link
                href="/courses"
                className="hover:text-primary transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                코스
              </Link>
              <Link
                href="/about"
                className="hover:text-primary transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                소개
              </Link>
              <Link
                href="/pricing"
                className="hover:text-primary transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                가격
              </Link>
              <div className="flex flex-col gap-2 pt-4 border-t">
                <Link href="/auth/login" onClick={() => setIsMenuOpen(false)}>
                  <Button variant="ghost" className="w-full">
                    로그인
                  </Button>
                </Link>
                <Link href="/auth/register" onClick={() => setIsMenuOpen(false)}>
                  <Button className="w-full">시작하기</Button>
                </Link>
              </div>
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}
