import Image from 'next/image'
import Link from 'next/link'
import { Course } from '@/types'
import { Card, CardContent, CardFooter } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { formatPrice, getDifficultyColor } from '@/lib/utils'
import { BookOpen, Users, Star } from 'lucide-react'

interface CourseCardProps {
  course: Course
}

export function CourseCard({ course }: CourseCardProps) {
  return (
    <Link href={`/courses/${course.slug}`}>
      <Card className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer h-full">
        <div className="relative h-48 w-full bg-gray-200">
          {course.thumbnail ? (
            <Image
              src={course.thumbnail}
              alt={course.title}
              fill
              className="object-cover"
            />
          ) : (
            <div className="flex items-center justify-center h-full">
              <BookOpen className="w-16 h-16 text-gray-400" />
            </div>
          )}
          <div className="absolute top-2 right-2">
            <Badge className={getDifficultyColor(course.difficulty)}>
              {course.difficulty === 'beginner' && '초급'}
              {course.difficulty === 'intermediate' && '중급'}
              {course.difficulty === 'advanced' && '고급'}
            </Badge>
          </div>
        </div>

        <CardContent className="p-4">
          <h3 className="font-semibold text-lg mb-2 line-clamp-2">
            {course.title}
          </h3>
          <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
            {course.short_description}
          </p>
          <p className="text-sm text-muted-foreground mb-2">
            {course.instructor_name}
          </p>

          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
              <span>{course.average_rating}</span>
              <span>({course.rating_count})</span>
            </div>
            <div className="flex items-center gap-1">
              <Users className="w-4 h-4" />
              <span>{course.total_enrollments.toLocaleString()}명</span>
            </div>
          </div>
        </CardContent>

        <CardFooter className="p-4 pt-0 flex justify-between items-center">
          <div>
            {course.price_type === 'free' ? (
              <span className="text-lg font-bold text-green-600">무료</span>
            ) : course.discount_price ? (
              <div className="flex items-baseline gap-2">
                <span className="text-lg font-bold">
                  {formatPrice(course.discount_price)}
                </span>
                <span className="text-sm line-through text-muted-foreground">
                  {formatPrice(course.price)}
                </span>
              </div>
            ) : (
              <span className="text-lg font-bold">
                {formatPrice(course.price)}
              </span>
            )}
          </div>
          <Badge variant="outline">{course.category}</Badge>
        </CardFooter>
      </Card>
    </Link>
  )
}
