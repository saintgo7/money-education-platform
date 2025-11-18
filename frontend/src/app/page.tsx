export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">
          Money Education Platform
        </h1>
        <p className="text-xl text-muted-foreground mb-8">
          AI 기반 온라인 교육 플랫폼
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/courses"
            className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:opacity-90"
          >
            코스 둘러보기
          </a>
          <a
            href="/auth/login"
            className="px-6 py-3 bg-secondary text-secondary-foreground rounded-lg hover:opacity-90"
          >
            로그인
          </a>
        </div>
      </div>
    </main>
  )
}
