'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { api } from '@/lib/api'
import { Plus, GripVertical, Trash2, Video, FileText, List, Award } from 'lucide-react'

interface Module {
  id?: number
  title: string
  description: string
  order: number
  lessons: Lesson[]
}

interface Lesson {
  id?: number
  title: string
  lesson_type: string
  order: number
  content?: string
  video_url?: string
  video_duration?: number
  is_preview: boolean
}

export default function CourseEditPage() {
  const params = useParams()
  const [modules, setModules] = useState<Module[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCurriculum()
  }, [])

  const fetchCurriculum = async () => {
    try {
      const response = await api.get(`/courses/courses/${params.id}/curriculum/`)
      setModules(response.data || [])
    } catch (error) {
      console.error('Failed to fetch curriculum:', error)
    } finally {
      setLoading(false)
    }
  }

  const addModule = () => {
    setModules([...modules, {
      title: '',
      description: '',
      order: modules.length,
      lessons: []
    }])
  }

  const updateModule = (index: number, field: string, value: any) => {
    const updated = [...modules]
    updated[index] = { ...updated[index], [field]: value }
    setModules(updated)
  }

  const deleteModule = (index: number) => {
    setModules(modules.filter((_, i) => i !== index))
  }

  const addLesson = (moduleIndex: number) => {
    const updated = [...modules]
    updated[moduleIndex].lessons.push({
      title: '',
      lesson_type: 'video',
      order: updated[moduleIndex].lessons.length,
      is_preview: false
    })
    setModules(updated)
  }

  const updateLesson = (moduleIndex: number, lessonIndex: number, field: string, value: any) => {
    const updated = [...modules]
    updated[moduleIndex].lessons[lessonIndex] = {
      ...updated[moduleIndex].lessons[lessonIndex],
      [field]: value
    }
    setModules(updated)
  }

  const deleteLesson = (moduleIndex: number, lessonIndex: number) => {
    const updated = [...modules]
    updated[moduleIndex].lessons = updated[moduleIndex].lessons.filter((_, i) => i !== lessonIndex)
    setModules(updated)
  }

  const saveCurriculum = async () => {
    try {
      // Save modules and lessons
      for (const module of modules) {
        if (module.id) {
          await api.patch(`/courses/modules/${module.id}/`, module)
        } else {
          const response = await api.post('/courses/modules/', {
            ...module,
            course: params.id
          })
          module.id = response.data.id
        }

        // Save lessons
        for (const lesson of module.lessons) {
          if (lesson.id) {
            await api.patch(`/courses/lessons/${lesson.id}/`, lesson)
          } else {
            await api.post('/courses/lessons/', {
              ...lesson,
              module: module.id
            })
          }
        }
      }

      alert('커리큘럼이 저장되었습니다!')
    } catch (error) {
      console.error('Failed to save curriculum:', error)
      alert('저장에 실패했습니다.')
    }
  }

  const getLessonIcon = (type: string) => {
    switch (type) {
      case 'video': return <Video className="w-4 h-4" />
      case 'text': return <FileText className="w-4 h-4" />
      case 'quiz': return <List className="w-4 h-4" />
      case 'assignment': return <Award className="w-4 h-4" />
      default: return <FileText className="w-4 h-4" />
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-5xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">커리큘럼 편집</h1>
          <div className="flex gap-2">
            <Button onClick={saveCurriculum}>저장</Button>
            <Button variant="outline" onClick={addModule}>
              <Plus className="w-4 h-4 mr-2" />
              모듈 추가
            </Button>
          </div>
        </div>

        {loading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 animate-pulse rounded-lg" />
            ))}
          </div>
        ) : modules.length > 0 ? (
          <div className="space-y-6">
            {modules.map((module, moduleIndex) => (
              <Card key={moduleIndex}>
                <CardHeader className="bg-gray-50">
                  <div className="flex items-start gap-4">
                    <GripVertical className="w-5 h-5 text-gray-400 mt-1" />
                    <div className="flex-1 space-y-4">
                      <Input
                        value={module.title}
                        onChange={(e) => updateModule(moduleIndex, 'title', e.target.value)}
                        placeholder="모듈 제목"
                        className="font-semibold"
                      />
                      <Input
                        value={module.description}
                        onChange={(e) => updateModule(moduleIndex, 'description', e.target.value)}
                        placeholder="모듈 설명"
                      />
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => deleteModule(moduleIndex)}
                    >
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </Button>
                  </div>
                </CardHeader>

                <CardContent className="pt-4">
                  <div className="space-y-3">
                    {module.lessons.map((lesson, lessonIndex) => (
                      <div key={lessonIndex} className="flex items-center gap-3 p-3 border rounded-lg">
                        <GripVertical className="w-4 h-4 text-gray-400" />
                        {getLessonIcon(lesson.lesson_type)}

                        <Input
                          value={lesson.title}
                          onChange={(e) => updateLesson(moduleIndex, lessonIndex, 'title', e.target.value)}
                          placeholder="레슨 제목"
                          className="flex-1"
                        />

                        <select
                          className="border rounded px-2 py-1 text-sm"
                          value={lesson.lesson_type}
                          onChange={(e) => updateLesson(moduleIndex, lessonIndex, 'lesson_type', e.target.value)}
                        >
                          <option value="video">동영상</option>
                          <option value="text">텍스트</option>
                          <option value="quiz">퀴즈</option>
                          <option value="assignment">과제</option>
                        </select>

                        <label className="flex items-center gap-1 text-sm">
                          <input
                            type="checkbox"
                            checked={lesson.is_preview}
                            onChange={(e) => updateLesson(moduleIndex, lessonIndex, 'is_preview', e.target.checked)}
                          />
                          미리보기
                        </label>

                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => deleteLesson(moduleIndex, lessonIndex)}
                        >
                          <Trash2 className="w-4 h-4 text-red-500" />
                        </Button>
                      </div>
                    ))}

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => addLesson(moduleIndex)}
                      className="w-full"
                    >
                      <Plus className="w-4 h-4 mr-2" />
                      레슨 추가
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="p-12 text-center">
              <h3 className="text-lg font-semibold mb-2">커리큘럼이 비어있습니다</h3>
              <p className="text-muted-foreground mb-4">
                모듈과 레슨을 추가하여 코스를 구성하세요
              </p>
              <Button onClick={addModule}>
                <Plus className="w-4 h-4 mr-2" />
                첫 모듈 추가
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
