'use client'

import { useState } from 'react'
import { Button } from './ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card'
import { Assignment, Submission } from '@/types'
import { Upload, FileText, Calendar, Award, CheckCircle } from 'lucide-react'
import { formatDate } from '@/lib/utils'
import { cn } from '@/lib/utils'

interface AssignmentSubmissionProps {
  assignment: Assignment
  existingSubmission?: Submission
  onSubmit: (content: string, file?: File) => Promise<void>
}

export function AssignmentSubmission({
  assignment,
  existingSubmission,
  onSubmit,
}: AssignmentSubmissionProps) {
  const [content, setContent] = useState(existingSubmission?.content || '')
  const [file, setFile] = useState<File | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]

      // Validate file size (max 10MB)
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError('파일 크기는 10MB를 초과할 수 없습니다.')
        return
      }

      setFile(selectedFile)
      setError('')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!content.trim() && !file) {
      setError('제출 내용 또는 파일을 추가해주세요.')
      return
    }

    setIsSubmitting(true)
    setError('')

    try {
      await onSubmit(content, file || undefined)
    } catch (err: any) {
      setError(err.message || '제출에 실패했습니다.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const isDueDatePassed = assignment.due_date && new Date(assignment.due_date) < new Date()
  const isGraded = existingSubmission?.graded_at

  return (
    <div className="space-y-6">
      {/* Assignment Details */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>{assignment.title}</span>
            <div className="flex items-center gap-2 text-sm font-normal">
              <Award className="w-4 h-4" />
              <span>{assignment.max_points}점</span>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground whitespace-pre-line mb-4">
            {assignment.description}
          </p>

          {assignment.due_date && (
            <div className="flex items-center gap-2 text-sm">
              <Calendar className="w-4 h-4" />
              <span>
                마감일: {formatDate(assignment.due_date)}
                {isDueDatePassed && (
                  <span className="ml-2 text-red-500">(마감됨)</span>
                )}
              </span>
            </div>
          )}

          {assignment.rubric && (
            <div className="mt-4">
              <h4 className="font-semibold mb-2">채점 기준</h4>
              <div className="bg-gray-50 p-4 rounded-lg">
                <pre className="text-sm whitespace-pre-wrap">
                  {JSON.stringify(assignment.rubric, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Existing Submission */}
      {existingSubmission && (
        <Card className={cn(
          'border-2',
          isGraded ? 'border-green-500' : 'border-blue-500'
        )}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              제출 완료
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">제출 내용</h4>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="whitespace-pre-line">{existingSubmission.content}</p>
              </div>
            </div>

            {existingSubmission.file_url && (
              <div>
                <h4 className="font-semibold mb-2">첨부 파일</h4>
                <a
                  href={existingSubmission.file_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-blue-600 hover:underline"
                >
                  <FileText className="w-4 h-4" />
                  파일 다운로드
                </a>
              </div>
            )}

            <div className="text-sm text-muted-foreground">
              제출 시간: {formatDate(existingSubmission.submitted_at)}
            </div>

            {isGraded && (
              <div className="border-t pt-4">
                <h4 className="font-semibold mb-2">채점 결과</h4>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span>점수</span>
                    <span className="text-2xl font-bold text-green-600">
                      {existingSubmission.score} / {assignment.max_points}
                    </span>
                  </div>
                  {existingSubmission.feedback && (
                    <div>
                      <h5 className="text-sm font-medium mb-1">피드백</h5>
                      <div className="bg-blue-50 p-3 rounded-lg text-sm">
                        {existingSubmission.feedback}
                      </div>
                    </div>
                  )}
                  <div className="text-sm text-muted-foreground">
                    채점 시간: {formatDate(existingSubmission.graded_at!)}
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Submission Form */}
      {!existingSubmission && (
        <Card>
          <CardHeader>
            <CardTitle>과제 제출</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              <div>
                <label className="block text-sm font-medium mb-2">
                  제출 내용 <span className="text-red-500">*</span>
                </label>
                <textarea
                  className="w-full border rounded-lg p-3 min-h-[200px]"
                  placeholder="과제 내용을 작성하세요..."
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  disabled={isSubmitting || isDueDatePassed}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  파일 첨부 (선택사항)
                </label>
                <div className="border-2 border-dashed rounded-lg p-6">
                  <input
                    type="file"
                    onChange={handleFileChange}
                    disabled={isSubmitting || isDueDatePassed}
                    className="hidden"
                    id="file-upload"
                  />
                  <label
                    htmlFor="file-upload"
                    className="flex flex-col items-center cursor-pointer"
                  >
                    <Upload className="w-8 h-8 text-gray-400 mb-2" />
                    <span className="text-sm text-muted-foreground">
                      {file ? file.name : '파일을 선택하거나 드래그하세요'}
                    </span>
                    <span className="text-xs text-muted-foreground mt-1">
                      최대 10MB
                    </span>
                  </label>
                </div>
              </div>

              <div className="flex items-center justify-between pt-4">
                <p className="text-sm text-muted-foreground">
                  제출 후에는 수정할 수 없습니다.
                </p>
                <Button
                  type="submit"
                  disabled={isSubmitting || isDueDatePassed}
                  size="lg"
                >
                  {isSubmitting ? '제출 중...' : '과제 제출'}
                </Button>
              </div>

              {isDueDatePassed && (
                <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
                  마감일이 지나 과제를 제출할 수 없습니다.
                </div>
              )}
            </form>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
