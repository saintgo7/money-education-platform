'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { analyticsApi, coursesApi } from '@/lib/api'
import { Course } from '@/types'
import { BookOpen, Users, DollarSign, Star, Plus } from 'lucide-react'
import { formatPrice } from '@/lib/utils'

export default function InstructorDashboard() {
  const [stats, setStats] = useState<any>(null)
  const [courses, setCourses] = useState<Course[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [statsResponse, coursesResponse] = await Promise.all([
        analyticsApi.getInstructorStats(),
        coursesApi.list({ ordering: '-created_at' }),
      ])

      setStats(statsResponse.data)
      setCourses(coursesResponse.data.results || coursesResponse.data)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/3" />
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded-lg" />
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">강사 대시보드</h1>
          <p className="text-muted-foreground">
            코스 성과와 학생들의 학습 현황을 확인하세요
          </p>
        </div>
        <Link href="/instructor/courses/new">
          <Button size="lg">
            <Plus className="w-4 h-4 mr-2" />
            새 코스 만들기
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">총 코스</p>
                <p className="text-3xl font-bold">{courses.length}</p>
              </div>
              <BookOpen className="w-10 h-10 text-blue-500 opacity-20" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">총 학생</p>
                <p className="text-3xl font-bold">
                  {stats?.total_students || 0}
                </p>
              </div>
              <Users className="w-10 h-10 text-green-500 opacity-20" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">총 수익</p>
                <p className="text-3xl font-bold">
                  {formatPrice(stats?.total_revenue || 0)}
                </p>
              </div>
              <DollarSign className="w-10 h-10 text-yellow-500 opacity-20" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">평균 평점</p>
                <p className="text-3xl font-bold">
                  {stats?.average_rating || '0.0'}
                </p>
              </div>
              <Star className="w-10 h-10 text-purple-500 opacity-20" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Courses List */}
      <Card>
        <CardHeader>
          <CardTitle>내 코스</CardTitle>
        </CardHeader>
        <CardContent>
          {courses.length === 0 ? (
            <div className="text-center py-16">
              <BookOpen className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <h3 className="text-lg font-semibold mb-2">
                아직 코스가 없습니다
              </h3>
              <p className="text-muted-foreground mb-6">
                첫 코스를 만들어 학생들과 지식을 공유하세요
              </p>
              <Link href="/instructor/courses/new">
                <Button>
                  <Plus className="w-4 h-4 mr-2" />
                  코스 만들기
                </Button>
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {courses.map((course) => (
                <div
                  key={course.id}
                  className="border rounded-lg p-4 flex items-center justify-between hover:bg-gray-50 transition"
                >
                  <div>
                    <h3 className="font-semibold mb-1">{course.title}</h3>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Users className="w-4 h-4" />
                        {course.total_enrollments} 학생
                      </span>
                      <span className="flex items-center gap-1">
                        <Star className="w-4 h-4" />
                        {course.average_rating} ({course.rating_count})
                      </span>
                      <span className={`px-2 py-1 rounded text-xs ${
                        course.is_published
                          ? 'bg-green-100 text-green-700'
                          : 'bg-yellow-100 text-yellow-700'
                      }`}>
                        {course.is_published ? '게시됨' : '초안'}
                      </span>
                    </div>
                  </div>
                  <Link href={`/instructor/courses/${course.id}`}>
                    <Button variant="outline">관리</Button>
                  </Link>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
