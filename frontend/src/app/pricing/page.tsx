import Link from 'next/link'
import { Button } from '@/components/ui/Button'
import { Check } from 'lucide-react'

export default function PricingPage() {
  const plans = [
    {
      name: 'Free',
      price: '무료',
      period: '',
      features: [
        '무료 코스 접근',
        'AI 튜터 (월 10회)',
        '커뮤니티 포럼',
        '기본 진도 추적',
      ],
      cta: '시작하기',
      popular: false,
    },
    {
      name: 'Pro',
      price: '₩19,000',
      period: '/월',
      features: [
        '모든 코스 무제한 접근',
        'AI 튜터 무제한',
        '인증서 발급',
        '오프라인 다운로드',
        '우선 질문 답변',
        '고급 분석',
      ],
      cta: '시작하기',
      popular: true,
    },
    {
      name: 'Team',
      price: '₩49,000',
      period: '/월/인',
      features: [
        'Pro의 모든 기능',
        '팀 관리 대시보드',
        '학습 경로 할당',
        '진도 리포트',
        '관리자 도구',
        '전담 지원',
        'SSO (10인 이상)',
      ],
      cta: '문의하기',
      popular: false,
    },
  ]

  return (
    <div className="container mx-auto px-4 py-16">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">합리적인 가격으로 시작하세요</h1>
        <p className="text-xl text-muted-foreground">
          필요에 맞는 플랜을 선택하고 지금 바로 학습을 시작하세요
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
        {plans.map((plan) => (
          <div
            key={plan.name}
            className={`rounded-lg border-2 p-8 relative ${
              plan.popular ? 'border-primary shadow-lg' : 'border-gray-200'
            }`}
          >
            {plan.popular && (
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-white px-4 py-1 rounded-full text-sm">
                가장 인기있는
              </div>
            )}

            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <div className="text-4xl font-bold mb-1">
                {plan.price}
                {plan.period && (
                  <span className="text-lg text-muted-foreground">{plan.period}</span>
                )}
              </div>
            </div>

            <ul className="space-y-3 mb-8">
              {plan.features.map((feature, index) => (
                <li key={index} className="flex items-start gap-2">
                  <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                  <span>{feature}</span>
                </li>
              ))}
            </ul>

            <Link href={plan.name === 'Team' ? '/contact' : '/auth/register'}>
              <Button
                className="w-full"
                variant={plan.popular ? 'default' : 'outline'}
              >
                {plan.cta}
              </Button>
            </Link>
          </div>
        ))}
      </div>

      {/* FAQ */}
      <div className="max-w-3xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-8">자주 묻는 질문</h2>

        <div className="space-y-4">
          <div className="border rounded-lg p-6">
            <h3 className="font-semibold mb-2">언제든지 플랜을 변경할 수 있나요?</h3>
            <p className="text-muted-foreground">
              네, 언제든지 플랜을 업그레이드하거나 다운그레이드할 수 있습니다.
              변경 사항은 즉시 적용됩니다.
            </p>
          </div>

          <div className="border rounded-lg p-6">
            <h3 className="font-semibold mb-2">환불 정책은 어떻게 되나요?</h3>
            <p className="text-muted-foreground">
              구독 후 7일 이내에는 100% 환불이 가능합니다.
              자세한 내용은 이용약관을 참조하세요.
            </p>
          </div>

          <div className="border rounded-lg p-6">
            <h3 className="font-semibold mb-2">Team 플랜의 최소 인원은 몇 명인가요?</h3>
            <p className="text-muted-foreground">
              Team 플랜은 최소 3명부터 시작할 수 있습니다.
              더 많은 인원이 필요하시면 별도로 문의해주세요.
            </p>
          </div>

          <div className="border rounded-lg p-6">
            <h3 className="font-semibold mb-2">AI 튜터는 어떻게 작동하나요?</h3>
            <p className="text-muted-foreground">
              Claude AI를 기반으로 한 튜터가 24/7 질문에 답변하고
              개인화된 학습 경로를 제시합니다. Pro 플랜에서는 무제한으로 이용 가능합니다.
            </p>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="text-center mt-16">
        <h2 className="text-3xl font-bold mb-4">아직 고민 중이신가요?</h2>
        <p className="text-xl text-muted-foreground mb-6">
          무료로 시작하고 언제든지 업그레이드하세요
        </p>
        <Link href="/auth/register">
          <Button size="lg">무료로 시작하기</Button>
        </Link>
      </div>
    </div>
  )
}
