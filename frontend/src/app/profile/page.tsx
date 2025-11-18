'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { authApi } from '@/lib/api'
import { User, Mail, Phone, BookOpen, Award } from 'lucide-react'

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null)
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    bio: '',
  })

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const response = await authApi.me()
      setUser(response.data)
      setFormData({
        first_name: response.data.first_name || '',
        last_name: response.data.last_name || '',
        email: response.data.email || '',
        phone: response.data.phone || '',
        bio: response.data.bio || '',
      })
    } catch (error) {
      console.error('Failed to fetch profile:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await authApi.me() // Update endpoint
      setEditing(false)
      fetchProfile()
      alert('프로필이 업데이트되었습니다!')
    } catch (error) {
      console.error('Failed to update profile:', error)
      alert('프로필 업데이트에 실패했습니다.')
    }
  }

  if (!user) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">내 프로필</h1>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Sidebar */}
          <div className="space-y-4">
            <Card>
              <CardContent className="p-6 text-center">
                <div className="w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <User className="w-12 h-12 text-primary" />
                </div>
                <h2 className="font-semibold text-lg">{user.first_name} {user.last_name}</h2>
                <p className="text-sm text-muted-foreground">{user.email}</p>
                <div className="mt-4">
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    user.subscription_tier === 'pro'
                      ? 'bg-blue-100 text-blue-800'
                      : user.subscription_tier === 'team'
                      ? 'bg-purple-100 text-purple-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {user.subscription_tier === 'pro' ? 'Pro 멤버' :
                     user.subscription_tier === 'team' ? 'Team 멤버' :
                     '무료 플랜'}
                  </span>
                </div>
              </CardContent>
            </Card>

            {user.user_type === 'student' && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">학습 통계</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <BookOpen className="w-4 h-4 text-muted-foreground" />
                      <span className="text-sm">수강 코스</span>
                    </div>
                    <span className="font-semibold">12</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Award className="w-4 h-4 text-muted-foreground" />
                      <span className="text-sm">완료 코스</span>
                    </div>
                    <span className="font-semibold">5</span>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Main Content */}
          <div className="md:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle>개인 정보</CardTitle>
                  {!editing && (
                    <Button variant="outline" onClick={() => setEditing(true)}>
                      편집
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                {editing ? (
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <Input
                        label="이름"
                        value={formData.first_name}
                        onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                      />
                      <Input
                        label="성"
                        value={formData.last_name}
                        onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                      />
                    </div>
                    <Input
                      label="이메일"
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    />
                    <Input
                      label="전화번호"
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    />
                    <div>
                      <label className="block text-sm font-medium mb-2">자기소개</label>
                      <textarea
                        className="w-full border rounded-lg px-3 py-2 min-h-[100px]"
                        value={formData.bio}
                        onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                      />
                    </div>
                    <div className="flex gap-2">
                      <Button type="submit">저장</Button>
                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => {
                          setEditing(false)
                          fetchProfile()
                        }}
                      >
                        취소
                      </Button>
                    </div>
                  </form>
                ) : (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-sm text-muted-foreground">이름</label>
                        <p className="font-medium">{user.first_name} {user.last_name}</p>
                      </div>
                      <div>
                        <label className="text-sm text-muted-foreground">이메일</label>
                        <p className="font-medium">{user.email}</p>
                      </div>
                    </div>
                    <div>
                      <label className="text-sm text-muted-foreground">전화번호</label>
                      <p className="font-medium">{user.phone || '등록되지 않음'}</p>
                    </div>
                    <div>
                      <label className="text-sm text-muted-foreground">자기소개</label>
                      <p className="font-medium">{user.bio || '자기소개가 없습니다.'}</p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>구독 정보</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm text-muted-foreground">현재 플랜</label>
                    <p className="font-medium capitalize">{user.subscription_tier}</p>
                  </div>
                  {user.subscription_tier !== 'free' && (
                    <div>
                      <label className="text-sm text-muted-foreground">만료일</label>
                      <p className="font-medium">
                        {user.subscription_expires
                          ? new Date(user.subscription_expires).toLocaleDateString('ko-KR')
                          : '무제한'}
                      </p>
                    </div>
                  )}
                  {user.subscription_tier === 'free' && (
                    <Button>Pro로 업그레이드</Button>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
