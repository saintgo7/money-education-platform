'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { coursesApi } from '@/lib/api'
import { Course } from '@/types'
import { BookOpen, Users, DollarSign, TrendingUp, Plus } from 'lucide-react'

export default function InstructorDashboard() {
  const [courses, setCourses] = useState<Course[]>([])
  const [stats, setStats] = useState({
    totalCourses: 0,
    totalStudents: 0,
    totalRevenue: 0,
    avgRating: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      // Fetch instructor's courses
      const response = await coursesApi.myCourses()
      setCourses(response.data)

      // Calculate stats
      const totalStudents = response.data.reduce((sum: number, course: Course) =>
        sum + course.total_enrollments, 0
      )
      const avgRating = response.data.reduce((sum: number, course: Course) =>
        sum + parseFloat(course.average_rating), 0
      ) / response.data.length || 0

      setStats({
        totalCourses: response.data.length,
        totalStudents,
        totalRevenue: 0, // Will be calculated from payment data
        avgRating,
      })
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">강사 대시보드</h1>
          <p className="text-muted-foreground">코스 관리 및 통계를 확인하세요</p>
        </div>
        <Link href="/instructor/courses/new">
          <Button>
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
                <p className="text-sm text-muted-foreground">전체 코스</p>
                <p className="text-3xl font-bold">{stats.totalCourses}</p>
              </div>
              <BookOpen className="w-10 h-10 text-primary opacity-20" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">총 수강생</p>
                <p className="text-3xl font-bold">{stats.totalStudents}</p>
              </div>
              <Users className="w-10 h-10 text-blue-500 opacity-20" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">총 수익</p>
                <p className="text-3xl font-bold">₩{stats.totalRevenue.toLocaleString()}</p>
              </div>
              <DollarSign className="w-10 h-10 text-green-500 opacity-20" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">평균 평점</p>
                <p className="text-3xl font-bold">{stats.avgRating.toFixed(1)}</p>
              </div>
              <TrendingUp className="w-10 h-10 text-yellow-500 opacity-20" />
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
          {loading ? (
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-24 bg-gray-200 animate-pulse rounded" />
              ))}
            </div>
          ) : courses.length > 0 ? (
            <div className="space-y-4">
              {courses.map((course) => (
                <div key={course.id} className="border rounded-lg p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="font-semibold text-lg">{course.title}</h3>
                        <span className={`px-2 py-1 rounded text-xs ${
                          course.is_published
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {course.is_published ? '게시됨' : '초안'}
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-4 text-sm text-muted-foreground">
                        <div>
                          <span className="font-medium">{course.total_enrollments}</span> 수강생
                        </div>
                        <div>
                          <span className="font-medium">{course.average_rating}</span> ★ ({course.rating_count})
                        </div>
                        <div>
                          <span className="font-medium">{course.category}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Link href={`/instructor/courses/${course.id}/edit`}>
                        <Button variant="outline" size="sm">편집</Button>
                      </Link>
                      <Link href={`/instructor/courses/${course.id}/students`}>
                        <Button variant="outline" size="sm">수강생</Button>
                      </Link>
                      <Link href={`/courses/${course.slug}`}>
                        <Button variant="ghost" size="sm">보기</Button>
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <BookOpen className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <h3 className="text-lg font-semibold mb-2">아직 코스가 없습니다</h3>
              <p className="text-muted-foreground mb-4">
                첫 번째 코스를 만들고 학생들과 지식을 공유하세요
              </p>
              <Link href="/instructor/courses/new">
                <Button>
                  <Plus className="w-4 h-4 mr-2" />
                  코스 만들기
                </Button>
              </Link>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
