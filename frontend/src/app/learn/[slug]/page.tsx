'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Progress } from '@/components/ui/Progress'
import { api } from '@/lib/api'
import { Play, CheckCircle, Lock, FileText, List } from 'lucide-react'

interface Module {
  id: number
  title: string
  description: string
  lessons: Lesson[]
}

interface Lesson {
  id: number
  title: string
  lesson_type: string
  video_url?: string
  content?: string
  is_preview: boolean
}

export default function LearnPage() {
  const params = useParams()
  const [modules, setModules] = useState<Module[]>([])
  const [currentLesson, setCurrentLesson] = useState<Lesson | null>(null)
  const [progress, setProgress] = useState(0)
  const [completedLessons, setCompletedLessons] = useState<number[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCourse()
  }, [])

  const fetchCourse = async () => {
    try {
      const curriculumResponse = await api.get(`/courses/courses/${params.slug}/curriculum/`)
      setModules(curriculumResponse.data)

      if (curriculumResponse.data.length > 0 && curriculumResponse.data[0].lessons.length > 0) {
        setCurrentLesson(curriculumResponse.data[0].lessons[0])
      }

      // Fetch enrollment progress
      const enrollmentResponse = await api.get(`/courses/enrollments/`)
      const enrollment = enrollmentResponse.data.find((e: any) => e.course === params.slug)
      if (enrollment) {
        setProgress(enrollment.progress_percentage)
        setCompletedLessons(enrollment.completed_lessons || [])
      }
    } catch (error) {
      console.error('Failed to fetch course:', error)
    } finally {
      setLoading(false)
    }
  }

  const markLessonComplete = async (lessonId: number) => {
    try {
      await api.post(`/courses/lessons/${lessonId}/mark_complete/`)
      setCompletedLessons([...completedLessons, lessonId])
      // Refresh progress
      fetchCourse()
    } catch (error) {
      console.error('Failed to mark lesson complete:', error)
    }
  }

  const getLessonIcon = (lesson: Lesson, isCompleted: boolean) => {
    if (isCompleted) return <CheckCircle className="w-5 h-5 text-green-500" />

    switch (lesson.lesson_type) {
      case 'video': return <Play className="w-5 h-5" />
      case 'text': return <FileText className="w-5 h-5" />
      case 'quiz': return <List className="w-5 h-5" />
      default: return <FileText className="w-5 h-5" />
    }
  }

  return (
    <div className="flex h-[calc(100vh-4rem)]">
      {/* Sidebar - Curriculum */}
      <div className="w-80 border-r bg-gray-50 overflow-y-auto">
        <div className="p-4 border-b bg-white">
          <h2 className="font-semibold mb-2">코스 진도</h2>
          <Progress value={progress} className="mb-2" />
          <p className="text-sm text-muted-foreground">{progress.toFixed(0)}% 완료</p>
        </div>

        <div className="p-4 space-y-4">
          {modules.map((module) => (
            <div key={module.id}>
              <h3 className="font-semibold mb-2">{module.title}</h3>
              <div className="space-y-1">
                {module.lessons.map((lesson) => {
                  const isCompleted = completedLessons.includes(lesson.id)
                  const isCurrent = currentLesson?.id === lesson.id

                  return (
                    <button
                      key={lesson.id}
                      onClick={() => setCurrentLesson(lesson)}
                      className={`w-full flex items-center gap-3 p-2 rounded text-sm hover:bg-white transition-colors ${
                        isCurrent ? 'bg-white shadow-sm' : ''
                      }`}
                    >
                      {getLessonIcon(lesson, isCompleted)}
                      <span className={`flex-1 text-left ${isCompleted ? 'line-through' : ''}`}>
                        {lesson.title}
                      </span>
                      {!lesson.is_preview && !completedLessons.includes(lesson.id) && (
                        <Lock className="w-4 h-4 text-gray-400" />
                      )}
                    </button>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : currentLesson ? (
          <div className="max-w-4xl mx-auto p-8">
            <h1 className="text-3xl font-bold mb-4">{currentLesson.title}</h1>

            {/* Video Player */}
            {currentLesson.lesson_type === 'video' && currentLesson.video_url && (
              <div className="bg-black rounded-lg mb-6 aspect-video">
                <video
                  src={currentLesson.video_url}
                  controls
                  className="w-full h-full rounded-lg"
                />
              </div>
            )}

            {/* Text Content */}
            {currentLesson.lesson_type === 'text' && currentLesson.content && (
              <Card className="mb-6">
                <CardContent className="p-6">
                  <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: currentLesson.content }} />
                </CardContent>
              </Card>
            )}

            {/* Actions */}
            <div className="flex gap-4">
              {!completedLessons.includes(currentLesson.id) && (
                <Button onClick={() => markLessonComplete(currentLesson.id)}>
                  <CheckCircle className="w-4 h-4 mr-2" />
                  완료 표시
                </Button>
              )}
              <Button variant="outline">
                다음 레슨
              </Button>
            </div>

            {/* AI Tutor Quick Access */}
            <Card className="mt-8">
              <CardHeader>
                <CardTitle>궁금한 점이 있나요?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  AI 튜터에게 이 레슨에 대해 질문하세요
                </p>
                <Button variant="outline">
                  AI 튜터와 대화하기
                </Button>
              </CardContent>
            </Card>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-2">레슨을 선택하세요</h2>
              <p className="text-muted-foreground">
                왼쪽 목록에서 학습할 레슨을 선택하세요
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
