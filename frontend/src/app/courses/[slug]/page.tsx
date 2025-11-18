'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Image from 'next/image'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Card, CardContent } from '@/components/ui/Card'
import { coursesApi } from '@/lib/api'
import { Course } from '@/types'
import { BookOpen, Users, Star, Clock, Award } from 'lucide-react'
import { formatPrice, getDifficultyColor, formatDuration } from '@/lib/utils'

export default function CourseDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [course, setCourse] = useState<Course | null>(null)
  const [loading, setLoading] = useState(true)
  const [enrolling, setEnrolling] = useState(false)

  useEffect(() => {
    fetchCourse()
  }, [params.slug])

  const fetchCourse = async () => {
    try {
      const response = await coursesApi.get(params.slug as string)
      setCourse(response.data)
    } catch (error) {
      console.error('Failed to fetch course:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleEnroll = async () => {
    if (!course) return

    setEnrolling(true)
    try {
      await coursesApi.enroll(course.id.toString())
      router.push(`/learn/${course.slug}`)
    } catch (error) {
      console.error('Failed to enroll:', error)
      alert('수강 신청에 실패했습니다. 로그인 후 다시 시도해주세요.')
    } finally {
      setEnrolling(false)
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-96 bg-gray-200 rounded-lg mb-8" />
          <div className="h-8 bg-gray-200 rounded w-1/2 mb-4" />
          <div className="h-4 bg-gray-200 rounded w-3/4" />
        </div>
      </div>
    )
  }

  if (!course) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold mb-4">코스를 찾을 수 없습니다</h1>
        <Button onClick={() => router.push('/courses')}>
          코스 목록으로 돌아가기
        </Button>
      </div>
    )
  }

  return (
    <div>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="container mx-auto px-4 py-16">
          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div>
              <Badge className={getDifficultyColor(course.difficulty) + ' mb-4'}>
                {course.difficulty === 'beginner' && '초급'}
                {course.difficulty === 'intermediate' && '중급'}
                {course.difficulty === 'advanced' && '고급'}
              </Badge>
              <h1 className="text-4xl md:text-5xl font-bold mb-4">
                {course.title}
              </h1>
              <p className="text-xl mb-6 opacity-90">
                {course.short_description}
              </p>

              <div className="flex items-center gap-6 mb-6">
                <div className="flex items-center gap-2">
                  <Star className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                  <span className="font-semibold">{course.average_rating}</span>
                  <span className="opacity-75">({course.rating_count}개 평가)</span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  <span>{course.total_enrollments.toLocaleString()}명 수강</span>
                </div>
              </div>

              <p className="mb-6">
                강사: <span className="font-semibold">{course.instructor_name}</span>
              </p>

              <div className="flex items-center gap-4">
                <div className="text-3xl font-bold">
                  {course.price_type === 'free' ? (
                    '무료'
                  ) : course.discount_price ? (
                    <>
                      {formatPrice(course.discount_price)}
                      <span className="text-lg line-through opacity-75 ml-2">
                        {formatPrice(course.price)}
                      </span>
                    </>
                  ) : (
                    formatPrice(course.price)
                  )}
                </div>
              </div>

              <Button
                size="lg"
                className="mt-6 bg-white text-blue-600 hover:bg-gray-100"
                onClick={handleEnroll}
                disabled={enrolling}
              >
                {enrolling ? '등록 중...' : '지금 수강하기'}
              </Button>
            </div>

            <div className="relative h-96 rounded-lg overflow-hidden">
              {course.thumbnail ? (
                <Image
                  src={course.thumbnail}
                  alt={course.title}
                  fill
                  className="object-cover"
                />
              ) : (
                <div className="w-full h-full bg-white/10 flex items-center justify-center">
                  <BookOpen className="w-32 h-32 opacity-50" />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="md:col-span-2">
            <Card className="mb-8">
              <CardContent className="p-6">
                <h2 className="text-2xl font-bold mb-4">코스 소개</h2>
                <p className="text-muted-foreground whitespace-pre-line">
                  {course.description}
                </p>
              </CardContent>
            </Card>

            <Card className="mb-8">
              <CardContent className="p-6">
                <h2 className="text-2xl font-bold mb-4">학습 목표</h2>
                <ul className="space-y-2">
                  {course.learning_objectives?.map((objective, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <span className="text-green-500 mt-1">✓</span>
                      <span>{objective}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            {course.prerequisites && (
              <Card>
                <CardContent className="p-6">
                  <h2 className="text-2xl font-bold mb-4">사전 요구사항</h2>
                  <p className="text-muted-foreground">{course.prerequisites}</p>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar */}
          <div>
            <Card>
              <CardContent className="p-6">
                <h3 className="font-semibold mb-4">코스 정보</h3>
                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                    <Clock className="w-5 h-5 text-muted-foreground" />
                    <div>
                      <div className="text-sm text-muted-foreground">총 학습 시간</div>
                      <div className="font-medium">
                        {formatDuration(course.total_duration_minutes * 60)}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <BookOpen className="w-5 h-5 text-muted-foreground" />
                    <div>
                      <div className="text-sm text-muted-foreground">카테고리</div>
                      <div className="font-medium">{course.category}</div>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <Award className="w-5 h-5 text-muted-foreground" />
                    <div>
                      <div className="text-sm text-muted-foreground">수료증</div>
                      <div className="font-medium">발급 가능</div>
                    </div>
                  </div>
                </div>

                <Button className="w-full mt-6" onClick={handleEnroll} disabled={enrolling}>
                  {enrolling ? '등록 중...' : '수강 신청'}
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
