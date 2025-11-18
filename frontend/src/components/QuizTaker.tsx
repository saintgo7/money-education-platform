'use client'

import { useState, useEffect } from 'react'
import { Button } from './ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card'
import { Quiz, QuizQuestion, QuizAttempt } from '@/types'
import { Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react'
import { cn } from '@/lib/utils'

interface QuizTakerProps {
  quiz: Quiz
  onSubmit: (answers: Record<number, string>) => void
  onComplete?: (attempt: QuizAttempt) => void
}

export function QuizTaker({ quiz, onSubmit, onComplete }: QuizTakerProps) {
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [timeLeft, setTimeLeft] = useState(quiz.time_limit_minutes * 60)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [showResults, setShowResults] = useState(false)

  const questions = quiz.questions || []

  useEffect(() => {
    if (quiz.time_limit_minutes > 0 && !isSubmitted) {
      const timer = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            handleSubmit()
            return 0
          }
          return prev - 1
        })
      }, 1000)

      return () => clearInterval(timer)
    }
  }, [quiz.time_limit_minutes, isSubmitted])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const handleAnswerChange = (questionId: number, answer: string) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: answer,
    }))
  }

  const handleSubmit = () => {
    setIsSubmitted(true)
    onSubmit(answers)
    setShowResults(true)
  }

  const getProgress = () => {
    const answeredCount = Object.keys(answers).length
    return Math.round((answeredCount / questions.length) * 100)
  }

  const renderQuestion = (question: QuizQuestion, index: number) => {
    const currentAnswer = answers[question.id]

    return (
      <Card key={question.id} className={index === currentQuestion ? 'border-blue-500' : ''}>
        <CardHeader>
          <CardTitle className="flex items-start justify-between">
            <span className="text-lg">
              질문 {index + 1}. {question.question_text}
            </span>
            <span className="text-sm font-normal text-muted-foreground">
              {question.points}점
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {question.question_type === 'multiple_choice' && (
            <div className="space-y-2">
              {question.options?.map((option, idx) => (
                <label
                  key={idx}
                  className={cn(
                    'flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition',
                    currentAnswer === option && 'bg-blue-50 border-blue-500'
                  )}
                >
                  <input
                    type="radio"
                    name={`question-${question.id}`}
                    value={option}
                    checked={currentAnswer === option}
                    onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                    disabled={isSubmitted}
                    className="w-4 h-4"
                  />
                  <span>{option}</span>
                </label>
              ))}
            </div>
          )}

          {question.question_type === 'true_false' && (
            <div className="space-y-2">
              {['True', 'False'].map((option) => (
                <label
                  key={option}
                  className={cn(
                    'flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition',
                    currentAnswer === option && 'bg-blue-50 border-blue-500'
                  )}
                >
                  <input
                    type="radio"
                    name={`question-${question.id}`}
                    value={option}
                    checked={currentAnswer === option}
                    onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                    disabled={isSubmitted}
                    className="w-4 h-4"
                  />
                  <span>{option === 'True' ? '참' : '거짓'}</span>
                </label>
              ))}
            </div>
          )}

          {question.question_type === 'short_answer' && (
            <textarea
              className="w-full border rounded-lg p-3 min-h-[100px]"
              placeholder="답변을 입력하세요..."
              value={currentAnswer || ''}
              onChange={(e) => handleAnswerChange(question.id, e.target.value)}
              disabled={isSubmitted}
            />
          )}

          {showResults && question.correct_answer && (
            <div className="mt-4">
              {currentAnswer === question.correct_answer ? (
                <div className="flex items-center gap-2 text-green-600">
                  <CheckCircle className="w-5 h-5" />
                  <span className="font-medium">정답입니다!</span>
                </div>
              ) : (
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-red-600">
                    <XCircle className="w-5 h-5" />
                    <span className="font-medium">오답입니다</span>
                  </div>
                  <div className="text-sm text-muted-foreground">
                    정답: {question.correct_answer}
                  </div>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    )
  }

  if (questions.length === 0) {
    return (
      <Card>
        <CardContent className="p-8 text-center">
          <AlertCircle className="w-12 h-12 mx-auto mb-4 text-yellow-500" />
          <p className="text-muted-foreground">퀴즈 문제를 불러올 수 없습니다.</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-2xl font-bold">{quiz.title}</h2>
              <p className="text-muted-foreground">{quiz.description}</p>
            </div>
            {quiz.time_limit_minutes > 0 && !isSubmitted && (
              <div className="flex items-center gap-2 text-lg">
                <Clock className="w-5 h-5" />
                <span className={cn(
                  'font-mono font-bold',
                  timeLeft < 60 && 'text-red-500'
                )}>
                  {formatTime(timeLeft)}
                </span>
              </div>
            )}
          </div>

          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="flex items-center justify-between text-sm mb-2">
                <span>진행률</span>
                <span>{getProgress()}%</span>
              </div>
              <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-500 transition-all"
                  style={{ width: `${getProgress()}%` }}
                />
              </div>
            </div>
            <div className="text-sm text-muted-foreground">
              {Object.keys(answers).length} / {questions.length} 답변
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Questions */}
      <div className="space-y-4">
        {questions.map((question, index) => renderQuestion(question, index))}
      </div>

      {/* Submit Button */}
      {!isSubmitted && (
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <p className="text-sm text-muted-foreground">
                모든 문제에 답변하셨나요? 제출 후에는 수정할 수 없습니다.
              </p>
              <Button
                onClick={handleSubmit}
                disabled={Object.keys(answers).length === 0}
                size="lg"
              >
                퀴즈 제출
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Results Summary */}
      {showResults && (
        <Card className="border-blue-500">
          <CardContent className="p-6">
            <div className="text-center">
              <h3 className="text-xl font-bold mb-2">퀴즈 완료!</h3>
              <p className="text-muted-foreground mb-4">
                결과를 확인하려면 채점이 완료될 때까지 기다려주세요.
              </p>
              <Button onClick={() => window.location.reload()}>
                다시 풀기
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
