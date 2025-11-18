'use client'

import { useState } from 'react'
import { ChevronDown, ChevronRight, PlayCircle, FileText, CheckCircle, Lock, Clock } from 'lucide-react'
import { Module, Lesson } from '@/types'
import { formatDuration } from '@/lib/utils'
import { cn } from '@/lib/utils'

interface CourseCurriculumProps {
  modules: Module[]
  currentLessonId?: number
  onLessonClick?: (lessonId: number) => void
  showProgress?: boolean
  completedLessons?: number[]
  isEnrolled?: boolean
}

export function CourseCurriculum({
  modules,
  currentLessonId,
  onLessonClick,
  showProgress = false,
  completedLessons = [],
  isEnrolled = false,
}: CourseCurriculumProps) {
  const [expandedModules, setExpandedModules] = useState<Set<number>>(
    new Set(modules.map((m) => m.id))
  )

  const toggleModule = (moduleId: number) => {
    const newExpanded = new Set(expandedModules)
    if (newExpanded.has(moduleId)) {
      newExpanded.delete(moduleId)
    } else {
      newExpanded.add(moduleId)
    }
    setExpandedModules(newExpanded)
  }

  const getLessonIcon = (lesson: Lesson) => {
    if (showProgress && completedLessons.includes(lesson.id)) {
      return <CheckCircle className="w-5 h-5 text-green-500" />
    }

    switch (lesson.lesson_type) {
      case 'video':
        return <PlayCircle className="w-5 h-5 text-blue-500" />
      case 'text':
        return <FileText className="w-5 h-5 text-gray-500" />
      case 'quiz':
      case 'assignment':
        return <FileText className="w-5 h-5 text-purple-500" />
      default:
        return <FileText className="w-5 h-5 text-gray-500" />
    }
  }

  const isLessonLocked = (lesson: Lesson) => {
    return !isEnrolled && !lesson.is_preview
  }

  const getTotalDuration = (module: Module) => {
    const totalSeconds = module.lessons.reduce((sum, lesson) => sum + lesson.video_duration, 0)
    return formatDuration(totalSeconds)
  }

  const getModuleProgress = (module: Module) => {
    if (!showProgress) return 0
    const completed = module.lessons.filter((l) => completedLessons.includes(l.id)).length
    return Math.round((completed / module.lessons.length) * 100)
  }

  return (
    <div className="space-y-2">
      {modules.map((module) => {
        const isExpanded = expandedModules.has(module.id)
        const progress = getModuleProgress(module)

        return (
          <div key={module.id} className="border rounded-lg overflow-hidden">
            {/* Module Header */}
            <button
              onClick={() => toggleModule(module.id)}
              className="w-full px-4 py-3 bg-gray-50 hover:bg-gray-100 flex items-center justify-between transition"
            >
              <div className="flex items-center gap-3">
                {isExpanded ? (
                  <ChevronDown className="w-5 h-5 text-gray-600" />
                ) : (
                  <ChevronRight className="w-5 h-5 text-gray-600" />
                )}
                <div className="text-left">
                  <h3 className="font-semibold">{module.title}</h3>
                  <p className="text-sm text-muted-foreground">
                    {module.lessons.length}개 레슨 · {getTotalDuration(module)}
                  </p>
                </div>
              </div>

              {showProgress && (
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">{progress}%</span>
                  <div className="w-16 h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-green-500 transition-all"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                </div>
              )}
            </button>

            {/* Lessons List */}
            {isExpanded && (
              <div className="divide-y">
                {module.lessons.map((lesson) => {
                  const isLocked = isLessonLocked(lesson)
                  const isCompleted = completedLessons.includes(lesson.id)
                  const isCurrent = currentLessonId === lesson.id

                  return (
                    <button
                      key={lesson.id}
                      onClick={() => !isLocked && onLessonClick?.(lesson.id)}
                      disabled={isLocked}
                      className={cn(
                        'w-full px-4 py-3 flex items-center justify-between hover:bg-gray-50 transition',
                        isCurrent && 'bg-blue-50 border-l-4 border-blue-500',
                        isLocked && 'opacity-60 cursor-not-allowed'
                      )}
                    >
                      <div className="flex items-center gap-3">
                        {getLessonIcon(lesson)}
                        <div className="text-left">
                          <div className="flex items-center gap-2">
                            <span className={cn(
                              'font-medium',
                              isCurrent && 'text-blue-600'
                            )}>
                              {lesson.title}
                            </span>
                            {lesson.is_preview && (
                              <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded">
                                미리보기
                              </span>
                            )}
                          </div>
                          {lesson.video_duration > 0 && (
                            <div className="flex items-center gap-1 text-sm text-muted-foreground">
                              <Clock className="w-3 h-3" />
                              {formatDuration(lesson.video_duration)}
                            </div>
                          )}
                        </div>
                      </div>

                      {isLocked && <Lock className="w-4 h-4 text-gray-400" />}
                    </button>
                  )
                })}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
