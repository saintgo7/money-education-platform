/**
 * TypeScript type definitions
 */

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  user_type: 'student' | 'instructor' | 'admin'
  avatar?: string
  bio?: string
  subscription_tier: 'free' | 'pro' | 'team'
}

export interface Course {
  id: number
  title: string
  slug: string
  description: string
  short_description: string
  instructor: number
  instructor_name: string
  thumbnail?: string
  category: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  price_type: 'free' | 'paid' | 'subscription'
  price: string
  discount_price?: string
  total_enrollments: number
  average_rating: string
  rating_count: number
  is_published: boolean
}

export interface Module {
  id: number
  course: number
  title: string
  description: string
  order: number
  lessons: Lesson[]
}

export interface Lesson {
  id: number
  module: number
  title: string
  lesson_type: 'video' | 'text' | 'quiz' | 'assignment' | 'live'
  order: number
  content?: string
  video_url?: string
  video_duration: number
  is_preview: boolean
}

export interface Enrollment {
  id: number
  student: number
  course: number
  course_title: string
  progress_percentage: number
  is_completed: boolean
  enrolled_at: string
}

export interface Conversation {
  id: number
  student: number
  course?: number
  lesson?: number
  title: string
  is_active: boolean
  created_at: string
}

export interface Message {
  id: number
  conversation: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface Quiz {
  id: number
  course: number
  title: string
  description: string
  passing_score: number
  time_limit_minutes: number
}

export interface Certificate {
  id: number
  student: number
  course: number
  student_name: string
  course_title: string
  certificate_id: string
  pdf_url: string
  issued_at: string
}
