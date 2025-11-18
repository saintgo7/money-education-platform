'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { VideoPlayer } from '@/components/VideoPlayer'
import { CourseCurriculum } from '@/components/CourseCurriculum'
import { QuizTaker } from '@/components/QuizTaker'
import { AssignmentSubmission } from '@/components/AssignmentSubmission'
import { Button } from '@/components/ui/Button'
import { Card, CardContent } from '@/components/ui/Card'
import { Progress } from '@/components/ui/Progress'
import { coursesApi, lessonsApi, assessmentApi } from '@/lib/api'
import { Module, Lesson } from '@/types'
import { ChevronLeft, ChevronRight, CheckCircle, MessageCircle } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import Link from 'next/link'

export default function LearnPage() {
  const params = useParams()
  const [modules, setModules] = useState<Module[]>([])
  const [currentLesson, setCurrentLesson] = useState<Lesson | null>(null)
  const [completedLessons, setCompletedLessons] = useState<number[]>([])
  const [loading, setLoading] = useState(true)
  const [showSidebar, setShowSidebar] = useState(true)
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    fetchCourseData()
  }, [params.courseSlug])

  const fetchCourseData = async () => {
    try {
      const course = await coursesApi.get(params.courseSlug as string)
      const curriculumResponse = await coursesApi.curriculum(course.data.id.toString())
      const moduleData = curriculumResponse.data

      setModules(moduleData)

      // Set first lesson as current
      if (moduleData.length > 0 && moduleData[0].lessons.length > 0) {
        setCurrentLesson(moduleData[0].lessons[0])
      }

      // TODO: Fetch completed lessons from enrollment progress
      setCompletedLessons([])
    } catch (error) {
      console.error('Failed to fetch course data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLessonClick = async (lessonId: number) => {
    const lesson = modules
      .flatMap((m) => m.lessons)
      .find((l) => l.id === lessonId)

    if (lesson) {
      setCurrentLesson(lesson)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  const handleLessonComplete = async () => {
    if (!currentLesson) return

    try {
      await lessonsApi.markComplete(currentLesson.id.toString())
      setCompletedLessons([...completedLessons, currentLesson.id])

      // Auto-advance to next lesson
      const nextLesson = getNextLesson()
      if (nextLesson) {
        setCurrentLesson(nextLesson)
      }
    } catch (error) {
      console.error('Failed to mark lesson complete:', error)
    }
  }

  const getNextLesson = (): Lesson | null => {
    if (!currentLesson) return null

    const allLessons = modules.flatMap((m) => m.lessons)
    const currentIndex = allLessons.findIndex((l) => l.id === currentLesson.id)

    if (currentIndex < allLessons.length - 1) {
      return allLessons[currentIndex + 1]
    }

    return null
  }

  const getPreviousLesson = (): Lesson | null => {
    if (!currentLesson) return null

    const allLessons = modules.flatMap((m) => m.lessons)
    const currentIndex = allLessons.findIndex((l) => l.id === currentLesson.id)

    if (currentIndex > 0) {
      return allLessons[currentIndex - 1]
    }

    return null
  }

  const calculateProgress = () => {
    const totalLessons = modules.reduce((sum, m) => sum + m.lessons.length, 0)
    if (totalLessons === 0) return 0
    return Math.round((completedLessons.length / totalLessons) * 100)
  }

  const isLessonCompleted = currentLesson && completedLessons.includes(currentLesson.id)
  const nextLesson = getNextLesson()
  const previousLesson = getPreviousLesson()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-muted-foreground">로딩 중...</p>
        </div>
      </div>
    )
  }

  if (!currentLesson) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">레슨을 찾을 수 없습니다</h2>
          <Button onClick={() => window.history.back()}>돌아가기</Button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-screen">
      {/* Main Content */}
      <div className="flex-1 overflow-y-auto">
        {/* Progress Bar */}
        <div className="bg-white border-b sticky top-0 z-10">
          <div className="container mx-auto px-4 py-3">
            <div className="flex items-center justify-between mb-2">
              <h2 className="font-semibold">{currentLesson.title}</h2>
              <span className="text-sm text-muted-foreground">
                {calculateProgress()}% 완료
              </span>
            </div>
            <Progress value={calculateProgress()} />
          </div>
        </div>

        <div className="container mx-auto px-4 py-8 max-w-5xl">
          {/* Video Player */}
          {currentLesson.lesson_type === 'video' && currentLesson.video_url && (
            <div className="mb-8">
              <VideoPlayer
                src={currentLesson.video_url}
                onComplete={handleLessonComplete}
                onProgress={(progress) => setProgress(progress)}
              />
            </div>
          )}

          {/* Text Content */}
          {currentLesson.lesson_type === 'text' && currentLesson.content && (
            <Card className="mb-8">
              <CardContent className="p-8 prose max-w-none">
                <ReactMarkdown>{currentLesson.content}</ReactMarkdown>
              </CardContent>
            </Card>
          )}

          {/* Quiz */}
          {currentLesson.lesson_type === 'quiz' && (
            <div className="mb-8">
              <QuizTaker
                quiz={{
                  id: 0,
                  course: 0,
                  title: currentLesson.title,
                  description: '',
                  passing_score: 70,
                  time_limit_minutes: 30,
                  questions: [],
                }}
                onSubmit={(answers) => {
                  console.log('Quiz submitted:', answers)
                  handleLessonComplete()
                }}
              />
            </div>
          )}

          {/* Assignment */}
          {currentLesson.lesson_type === 'assignment' && (
            <div className="mb-8">
              <AssignmentSubmission
                assignment={{
                  id: 0,
                  course: 0,
                  lesson: currentLesson.id,
                  title: currentLesson.title,
                  description: currentLesson.content || '',
                  max_points: 100,
                }}
                onSubmit={async (content, file) => {
                  console.log('Assignment submitted:', content, file)
                  handleLessonComplete()
                }}
              />
            </div>
          )}

          {/* Lesson Actions */}
          <div className="flex items-center justify-between border-t pt-6">
            <div>
              {previousLesson && (
                <Button
                  variant="outline"
                  onClick={() => handleLessonClick(previousLesson.id)}
                >
                  <ChevronLeft className="w-4 h-4 mr-2" />
                  이전 레슨
                </Button>
              )}
            </div>

            <div className="flex items-center gap-4">
              <Link href="/ai-tutor">
                <Button variant="outline">
                  <MessageCircle className="w-4 h-4 mr-2" />
                  AI 튜터에게 질문
                </Button>
              </Link>

              {!isLessonCompleted && (
                <Button onClick={handleLessonComplete}>
                  <CheckCircle className="w-4 h-4 mr-2" />
                  완료 표시
                </Button>
              )}

              {nextLesson && (
                <Button onClick={() => handleLessonClick(nextLesson.id)}>
                  다음 레슨
                  <ChevronRight className="w-4 h-4 ml-2" />
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Sidebar - Curriculum */}
      <div
        className={`bg-white border-l transition-all duration-300 ${
          showSidebar ? 'w-96' : 'w-0'
        } overflow-hidden`}
      >
        <div className="h-full overflow-y-auto p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">코스 콘텐츠</h3>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowSidebar(!showSidebar)}
            >
              {showSidebar ? '숨기기' : '보기'}
            </Button>
          </div>

          <CourseCurriculum
            modules={modules}
            currentLessonId={currentLesson.id}
            onLessonClick={handleLessonClick}
            showProgress
            completedLessons={completedLessons}
            isEnrolled
          />
        </div>
      </div>

      {/* Toggle Sidebar Button (when hidden) */}
      {!showSidebar && (
        <button
          onClick={() => setShowSidebar(true)}
          className="fixed right-4 top-20 bg-white border rounded-lg p-2 shadow-lg hover:bg-gray-50 transition z-20"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
      )}
    </div>
  )
}
