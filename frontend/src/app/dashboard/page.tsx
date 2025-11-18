'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Progress } from '@/components/ui/Progress'
import { coursesApi } from '@/lib/api'
import { Enrollment } from '@/types'
import { BookOpen, Trophy, Clock, Brain } from 'lucide-react'

export default function DashboardPage() {
  const [enrollments, setEnrollments] = useState<Enrollment[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchEnrollments()
  }, [])

  const fetchEnrollments = async () => {
    try {
      const response = await coursesApi.myCourses()
      setEnrollments(response.data)
    } catch (error) {
      console.error('Failed to fetch enrollments:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">학습 대시보드</h1>
        <p className="text-muted-foreground">학습 진도와 성과를 확인하세요</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">수강 중인 코스</p>
                <p className="text-3xl font-bold">{enrollments.length}</p>
              </div>
              <BookOpen className="w-10 h-10 text-primary opacity-20" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">완료한 코스</p>
                <p className="text-3xl font-bold">
                  {enrollments.filter(e => e.is_completed).length}
                </p>
              </div>
              <Trophy className="w-10 h-10 text-yellow-500 opacity-20" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">총 학습 시간</p>
                <p className="text-3xl font-bold">45h</p>
              </div>
              <Clock className="w-10 h-10 text-blue-500 opacity-20" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">AI 튜터 사용</p>
                <p className="text-3xl font-bold">32</p>
              </div>
              <Brain className="w-10 h-10 text-purple-500 opacity-20" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* My Courses */}
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
          ) : enrollments.length > 0 ? (
            <div className="space-y-4">
              {enrollments.map((enrollment) => (
                <div key={enrollment.id} className="border rounded-lg p-4">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="font-semibold">{enrollment.course_title}</h3>
                      <p className="text-sm text-muted-foreground">
                        진도: {enrollment.progress_percentage.toFixed(1)}%
                      </p>
                    </div>
                    <Link href={`/learn/${enrollment.course}`}>
                      <Button size="sm">계속 학습</Button>
                    </Link>
                  </div>
                  <Progress value={enrollment.progress_percentage} />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-muted-foreground mb-4">아직 수강 중인 코스가 없습니다</p>
              <Link href="/courses">
                <Button>코스 둘러보기</Button>
              </Link>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
