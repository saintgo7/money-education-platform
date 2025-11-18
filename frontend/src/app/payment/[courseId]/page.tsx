'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { coursesApi, paymentsApi } from '@/lib/api'
import { Course } from '@/types'
import { formatPrice } from '@/lib/utils'
import { CreditCard, Shield, CheckCircle } from 'lucide-react'
import Image from 'next/image'

export default function PaymentPage() {
  const params = useParams()
  const router = useRouter()
  const [course, setCourse] = useState<Course | null>(null)
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState(false)
  const [paymentMethod, setPaymentMethod] = useState<'stripe' | 'toss'>('stripe')

  useEffect(() => {
    fetchCourse()
  }, [params.courseId])

  const fetchCourse = async () => {
    try {
      const response = await coursesApi.get(params.courseId as string)
      setCourse(response.data)
    } catch (error) {
      console.error('Failed to fetch course:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePayment = async () => {
    if (!course) return

    setProcessing(true)

    try {
      if (paymentMethod === 'stripe') {
        const response = await paymentsApi.createStripeCheckout(course.id)
        window.location.href = response.data.checkout_url
      } else {
        const response = await paymentsApi.createTossPayment({
          course_id: course.id,
          amount: course.discount_price || course.price,
        })
        window.location.href = response.data.payment_url
      }
    } catch (error) {
      console.error('Payment failed:', error)
      alert('결제 처리 중 오류가 발생했습니다.')
      setProcessing(false)
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 rounded w-1/3" />
            <div className="h-64 bg-gray-200 rounded" />
          </div>
        </div>
      </div>
    )
  }

  if (!course) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold mb-4">코스를 찾을 수 없습니다</h1>
        <Button onClick={() => router.push('/courses')}>
          코스 목록으로 돌아가기
        </Button>
      </div>
    )
  }

  const finalPrice = course.discount_price || course.price
  const discount = course.discount_price
    ? ((parseFloat(course.price) - parseFloat(course.discount_price)) /
        parseFloat(course.price)) *
      100
    : 0

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">결제하기</h1>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Order Summary */}
          <div className="md:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>주문 내역</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4">
                  <div className="relative w-32 h-20 rounded-lg overflow-hidden bg-gray-100 flex-shrink-0">
                    {course.thumbnail && (
                      <Image
                        src={course.thumbnail}
                        alt={course.title}
                        fill
                        className="object-cover"
                      />
                    )}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold mb-1">{course.title}</h3>
                    <p className="text-sm text-muted-foreground">
                      강사: {course.instructor_name}
                    </p>
                  </div>
                  <div className="text-right">
                    {course.discount_price ? (
                      <div>
                        <div className="text-sm text-gray-500 line-through">
                          {formatPrice(parseFloat(course.price))}
                        </div>
                        <div className="text-lg font-bold text-red-500">
                          {formatPrice(parseFloat(course.discount_price))}
                        </div>
                        <div className="text-xs text-red-500">
                          {discount.toFixed(0)}% 할인
                        </div>
                      </div>
                    ) : (
                      <div className="text-lg font-bold">
                        {formatPrice(parseFloat(course.price))}
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>결제 방법</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <label
                  className={`flex items-center gap-3 p-4 border-2 rounded-lg cursor-pointer transition ${
                    paymentMethod === 'stripe'
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="payment"
                    value="stripe"
                    checked={paymentMethod === 'stripe'}
                    onChange={(e) => setPaymentMethod(e.target.value as 'stripe')}
                    className="w-4 h-4"
                  />
                  <CreditCard className="w-5 h-5" />
                  <div>
                    <div className="font-medium">신용카드 / 체크카드</div>
                    <div className="text-sm text-muted-foreground">
                      Stripe을 통한 안전한 결제
                    </div>
                  </div>
                </label>

                <label
                  className={`flex items-center gap-3 p-4 border-2 rounded-lg cursor-pointer transition ${
                    paymentMethod === 'toss'
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="payment"
                    value="toss"
                    checked={paymentMethod === 'toss'}
                    onChange={(e) => setPaymentMethod(e.target.value as 'toss')}
                    className="w-4 h-4"
                  />
                  <CreditCard className="w-5 h-5" />
                  <div>
                    <div className="font-medium">토스페이먼츠</div>
                    <div className="text-sm text-muted-foreground">
                      간편 결제 및 다양한 결제 수단
                    </div>
                  </div>
                </label>
              </CardContent>
            </Card>

            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Shield className="w-4 h-4" />
              <span>모든 결제는 SSL로 암호화되어 안전하게 처리됩니다</span>
            </div>
          </div>

          {/* Payment Summary */}
          <div>
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle>결제 금액</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">상품 가격</span>
                    <span>{formatPrice(parseFloat(course.price))}</span>
                  </div>
                  {course.discount_price && (
                    <div className="flex justify-between text-red-500">
                      <span>할인</span>
                      <span>
                        -{formatPrice(parseFloat(course.price) - parseFloat(course.discount_price))}
                      </span>
                    </div>
                  )}
                </div>

                <div className="border-t pt-4">
                  <div className="flex justify-between text-lg font-bold">
                    <span>최종 결제 금액</span>
                    <span className="text-blue-600">
                      {formatPrice(parseFloat(finalPrice))}
                    </span>
                  </div>
                </div>

                <Button
                  onClick={handlePayment}
                  disabled={processing}
                  className="w-full"
                  size="lg"
                >
                  {processing ? '처리 중...' : '결제하기'}
                </Button>

                <div className="space-y-2 text-xs text-muted-foreground">
                  <div className="flex items-start gap-2">
                    <CheckCircle className="w-3 h-3 mt-0.5 flex-shrink-0" />
                    <span>구매 후 즉시 코스에 액세스할 수 있습니다</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <CheckCircle className="w-3 h-3 mt-0.5 flex-shrink-0" />
                    <span>평생 소장 가능한 콘텐츠</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <CheckCircle className="w-3 h-3 mt-0.5 flex-shrink-0" />
                    <span>수료증 발급 가능</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
