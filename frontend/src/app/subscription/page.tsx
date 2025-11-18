'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { paymentsApi } from '@/lib/api'
import { CheckCircle, Crown, Zap } from 'lucide-react'
import { cn } from '@/lib/utils'

const plans = [
  {
    id: 'free',
    name: '무료',
    price: 0,
    description: '기본 기능을 무료로 사용하세요',
    features: [
      '무료 코스 액세스',
      '기본 AI 튜터 (월 10회)',
      '커뮤니티 액세스',
      '진도 추적',
    ],
    icon: CheckCircle,
    color: 'text-gray-600',
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 29000,
    description: '전문가를 위한 프리미엄 기능',
    features: [
      '모든 코스 무제한 액세스',
      '무제한 AI 튜터',
      '개인 맞춤 학습 경로',
      '우선 지원',
      '수료증 발급',
      '다운로드 가능한 콘텐츠',
    ],
    icon: Zap,
    color: 'text-blue-600',
    popular: true,
  },
  {
    id: 'team',
    name: 'Team',
    price: 99000,
    description: '팀과 조직을 위한 솔루션',
    features: [
      'Pro의 모든 기능',
      '최대 10명 팀원',
      '팀 분석 및 리포트',
      '전담 계정 관리자',
      '커스텀 학습 경로',
      '팀 협업 도구',
    ],
    icon: Crown,
    color: 'text-purple-600',
  },
]

export default function SubscriptionPage() {
  const [currentPlan, setCurrentPlan] = useState<string>('free')
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState(false)

  useEffect(() => {
    fetchSubscription()
  }, [])

  const fetchSubscription = async () => {
    try {
      const response = await paymentsApi.getSubscription()
      setCurrentPlan(response.data.plan || 'free')
    } catch (error) {
      console.error('Failed to fetch subscription:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubscribe = async (planId: string) => {
    if (planId === currentPlan) return

    setProcessing(true)

    try {
      if (planId === 'free') {
        await paymentsApi.cancelSubscription()
        setCurrentPlan('free')
        alert('구독이 취소되었습니다.')
      } else {
        const response = await paymentsApi.createSubscription(planId)
        window.location.href = response.data.checkout_url
      }
    } catch (error) {
      console.error('Subscription failed:', error)
      alert('구독 처리 중 오류가 발생했습니다.')
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-16">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">플랜 선택</h1>
          <p className="text-xl text-muted-foreground">
            학습 목표에 맞는 플랜을 선택하세요
          </p>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-96 bg-gray-200 animate-pulse rounded-lg" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {plans.map((plan) => {
              const Icon = plan.icon
              const isCurrentPlan = currentPlan === plan.id

              return (
                <Card
                  key={plan.id}
                  className={cn(
                    'relative overflow-hidden transition-all',
                    plan.popular && 'border-2 border-blue-500 shadow-lg scale-105',
                    isCurrentPlan && 'ring-2 ring-green-500'
                  )}
                >
                  {plan.popular && (
                    <div className="absolute top-0 right-0 bg-blue-500 text-white text-xs px-3 py-1 rounded-bl-lg">
                      인기
                    </div>
                  )}

                  {isCurrentPlan && (
                    <div className="absolute top-0 left-0 bg-green-500 text-white text-xs px-3 py-1 rounded-br-lg">
                      현재 플랜
                    </div>
                  )}

                  <CardHeader className="text-center">
                    <Icon className={cn('w-12 h-12 mx-auto mb-4', plan.color)} />
                    <CardTitle className="text-2xl mb-2">{plan.name}</CardTitle>
                    <p className="text-sm text-muted-foreground">
                      {plan.description}
                    </p>
                  </CardHeader>

                  <CardContent>
                    <div className="text-center mb-6">
                      <span className="text-4xl font-bold">
                        {plan.price.toLocaleString()}원
                      </span>
                      <span className="text-muted-foreground">/월</span>
                    </div>

                    <ul className="space-y-3 mb-6">
                      {plan.features.map((feature, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                          <span className="text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>

                    <Button
                      onClick={() => handleSubscribe(plan.id)}
                      disabled={processing || isCurrentPlan}
                      className="w-full"
                      variant={plan.popular ? 'default' : 'outline'}
                    >
                      {isCurrentPlan
                        ? '현재 플랜'
                        : plan.price === 0
                        ? '무료로 시작'
                        : '구독하기'}
                    </Button>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        )}

        <div className="mt-12 text-center">
          <p className="text-sm text-muted-foreground">
            모든 플랜은 언제든지 변경하거나 취소할 수 있습니다.
            <br />
            결제는 안전하게 암호화되어 처리됩니다.
          </p>
        </div>
      </div>
    </div>
  )
}
