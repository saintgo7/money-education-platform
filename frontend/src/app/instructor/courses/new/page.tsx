'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { api } from '@/lib/api'

export default function NewCoursePage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    short_description: '',
    description: '',
    category: 'programming',
    difficulty: 'beginner',
    price_type: 'free',
    price: '0',
    learning_objectives: [''],
    prerequisites: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await api.post('/courses/courses/', {
        ...formData,
        learning_objectives: formData.learning_objectives.filter(obj => obj.trim()),
      })

      router.push(`/instructor/courses/${response.data.id}/edit`)
    } catch (error) {
      console.error('Failed to create course:', error)
      alert('코스 생성에 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const addLearningObjective = () => {
    setFormData({
      ...formData,
      learning_objectives: [...formData.learning_objectives, '']
    })
  }

  const updateLearningObjective = (index: number, value: string) => {
    const objectives = [...formData.learning_objectives]
    objectives[index] = value
    setFormData({ ...formData, learning_objectives: objectives })
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">새 코스 만들기</h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>기본 정보</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input
                label="코스 제목"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                required
                placeholder="예: Python 완벽 가이드"
              />

              <div>
                <label className="block text-sm font-medium mb-2">
                  짧은 설명
                </label>
                <Input
                  value={formData.short_description}
                  onChange={(e) => setFormData({ ...formData, short_description: e.target.value })}
                  required
                  placeholder="한 줄로 코스를 설명하세요"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  상세 설명
                </label>
                <textarea
                  className="w-full border rounded-lg px-3 py-2 min-h-[150px]"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  required
                  placeholder="코스에 대해 자세히 설명하세요"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">
                    카테고리
                  </label>
                  <select
                    className="w-full border rounded-lg px-3 py-2"
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  >
                    <option value="programming">프로그래밍</option>
                    <option value="design">디자인</option>
                    <option value="business">비즈니스</option>
                    <option value="marketing">마케팅</option>
                    <option value="data-science">데이터 사이언스</option>
                    <option value="language">외국어</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    난이도
                  </label>
                  <select
                    className="w-full border rounded-lg px-3 py-2"
                    value={formData.difficulty}
                    onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
                  >
                    <option value="beginner">초급</option>
                    <option value="intermediate">중급</option>
                    <option value="advanced">고급</option>
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>학습 목표</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {formData.learning_objectives.map((objective, index) => (
                <Input
                  key={index}
                  value={objective}
                  onChange={(e) => updateLearningObjective(index, e.target.value)}
                  placeholder={`학습 목표 ${index + 1}`}
                />
              ))}
              <Button type="button" variant="outline" onClick={addLearningObjective}>
                + 학습 목표 추가
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>가격 설정</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  가격 유형
                </label>
                <select
                  className="w-full border rounded-lg px-3 py-2"
                  value={formData.price_type}
                  onChange={(e) => setFormData({ ...formData, price_type: e.target.value })}
                >
                  <option value="free">무료</option>
                  <option value="paid">유료</option>
                  <option value="subscription">구독 전용</option>
                </select>
              </div>

              {formData.price_type === 'paid' && (
                <Input
                  label="가격 (원)"
                  type="number"
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                  placeholder="49000"
                />
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>사전 요구사항</CardTitle>
            </CardHeader>
            <CardContent>
              <textarea
                className="w-full border rounded-lg px-3 py-2 min-h-[100px]"
                value={formData.prerequisites}
                onChange={(e) => setFormData({ ...formData, prerequisites: e.target.value })}
                placeholder="이 코스를 수강하기 위해 필요한 사전 지식이나 요구사항을 작성하세요"
              />
            </CardContent>
          </Card>

          <div className="flex gap-4">
            <Button type="submit" disabled={loading} className="flex-1">
              {loading ? '생성 중...' : '코스 생성'}
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => router.back()}
            >
              취소
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}
