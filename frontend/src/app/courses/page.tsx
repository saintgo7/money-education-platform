'use client'

import { useState, useEffect } from 'react'
import { CourseCard } from '@/components/CourseCard'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { coursesApi } from '@/lib/api'
import { Course } from '@/types'
import { Search } from 'lucide-react'

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [difficulty, setDifficulty] = useState('')

  useEffect(() => {
    fetchCourses()
  }, [category, difficulty])

  const fetchCourses = async () => {
    try {
      const response = await coursesApi.list({
        search,
        category,
        difficulty,
      })
      setCourses(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to fetch courses:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    fetchCourses()
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">모든 코스</h1>
        <p className="text-muted-foreground">
          전문가가 제작한 고품질 코스로 새로운 기술을 배우세요
        </p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg p-6 mb-8 border">
        <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground w-5 h-5" />
            <Input
              placeholder="코스 검색..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10"
            />
          </div>

          <select
            className="border rounded-lg px-4 py-2"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="">모든 카테고리</option>
            <option value="programming">프로그래밍</option>
            <option value="design">디자인</option>
            <option value="business">비즈니스</option>
            <option value="marketing">마케팅</option>
          </select>

          <select
            className="border rounded-lg px-4 py-2"
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          >
            <option value="">모든 난이도</option>
            <option value="beginner">초급</option>
            <option value="intermediate">중급</option>
            <option value="advanced">고급</option>
          </select>

          <Button type="submit">검색</Button>
        </form>
      </div>

      {/* Course Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="h-96 bg-gray-200 animate-pulse rounded-lg" />
          ))}
        </div>
      ) : courses.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {courses.map((course) => (
            <CourseCard key={course.id} course={course} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <p className="text-muted-foreground">검색 결과가 없습니다.</p>
        </div>
      )}
    </div>
  )
}
