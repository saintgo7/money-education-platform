import Link from 'next/link'
import { Button } from '@/components/ui/Button'
import { BookOpen, Brain, Trophy, Users } from 'lucide-react'

export default function Home() {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-b from-blue-50 to-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            AI와 함께하는
            <br />
            <span className="text-primary">개인화된 학습</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Claude AI 튜터가 당신의 학습 스타일에 맞춰 1:1 맞춤 교육을 제공합니다.
            언제 어디서나 궁금한 것을 물어보세요.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/courses">
              <Button size="lg">코스 둘러보기</Button>
            </Link>
            <Link href="/auth/register">
              <Button size="lg" variant="outline">
                무료로 시작하기
              </Button>
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16 max-w-4xl mx-auto">
            <div>
              <div className="text-3xl font-bold text-primary">1,000+</div>
              <div className="text-muted-foreground">온라인 코스</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">50,000+</div>
              <div className="text-muted-foreground">수강생</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">500+</div>
              <div className="text-muted-foreground">전문 강사</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">4.8/5</div>
              <div className="text-muted-foreground">평균 만족도</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            왜 Money Education을 선택해야 할까요?
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">AI 튜터</h3>
              <p className="text-muted-foreground">
                Claude AI가 24/7 당신의 질문에 답변하고 개인화된 학습 경로를 제시합니다.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <BookOpen className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">전문 코스</h3>
              <p className="text-muted-foreground">
                검증된 전문가들이 만든 고품질 교육 콘텐츠로 체계적으로 학습하세요.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Trophy className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">인증서</h3>
              <p className="text-muted-foreground">
                코스 완료 시 검증된 수료증을 발급받아 경력에 추가하세요.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">커뮤니티</h3>
              <p className="text-muted-foreground">
                같은 목표를 가진 학습자들과 함께 성장하는 커뮤니티에 참여하세요.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            합리적인 가격으로 시작하세요
          </h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {/* Free */}
            <div className="bg-white rounded-lg p-8 border-2">
              <h3 className="text-2xl font-bold mb-2">Free</h3>
              <div className="text-4xl font-bold mb-4">무료</div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>무료 코스 접근</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>AI 튜터 (월 10회)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>커뮤니티 포럼</span>
                </li>
              </ul>
              <Link href="/auth/register">
                <Button variant="outline" className="w-full">
                  시작하기
                </Button>
              </Link>
            </div>

            {/* Pro */}
            <div className="bg-white rounded-lg p-8 border-2 border-primary relative">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-white px-4 py-1 rounded-full text-sm">
                인기
              </div>
              <h3 className="text-2xl font-bold mb-2">Pro</h3>
              <div className="text-4xl font-bold mb-4">
                ₩19,000<span className="text-lg text-muted-foreground">/월</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>모든 코스 무제한</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>AI 튜터 무제한</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>인증서 발급</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>오프라인 다운로드</span>
                </li>
              </ul>
              <Link href="/auth/register">
                <Button className="w-full">시작하기</Button>
              </Link>
            </div>

            {/* Team */}
            <div className="bg-white rounded-lg p-8 border-2">
              <h3 className="text-2xl font-bold mb-2">Team</h3>
              <div className="text-4xl font-bold mb-4">
                ₩49,000<span className="text-lg text-muted-foreground">/월/인</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>Pro의 모든 기능</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>팀 관리 대시보드</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>학습 경로 할당</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>진도 리포트</span>
                </li>
              </ul>
              <Link href="/contact">
                <Button variant="outline" className="w-full">
                  문의하기
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">
            지금 바로 학습을 시작하세요
          </h2>
          <p className="text-xl text-muted-foreground mb-8">
            무료로 가입하고 AI 튜터와 함께 성장하세요
          </p>
          <Link href="/auth/register">
            <Button size="lg">무료로 시작하기</Button>
          </Link>
        </div>
      </section>
    </div>
  )
}
