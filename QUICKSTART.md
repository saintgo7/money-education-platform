# Quick Start Guide

빠르게 시작하는 가이드입니다.

## 사전 요구사항

- Docker & Docker Compose
- (선택) Python 3.11+, Node.js 18+, PostgreSQL, Redis

## Option 1: Docker로 시작 (추천)

### 1. 자동 설정 스크립트 실행

```bash
chmod +x setup.sh
./setup.sh
```

스크립트가 자동으로:
- 환경 파일 생성
- Docker 컨테이너 빌드 및 실행
- 데이터베이스 마이그레이션
- 샘플 데이터 생성 (선택)
- 슈퍼유저 생성 (선택)

### 2. 접속

```bash
# Frontend
http://localhost:3000

# Backend API
http://localhost:8000

# API 문서
http://localhost:8000/api/docs/

# Admin 패널
http://localhost:8000/admin/
```

### 3. 샘플 계정

설정 스크립트에서 샘플 데이터를 생성했다면:

```
학생: student@example.com / student123
강사: instructor@example.com / instructor123
관리자: admin@example.com / admin123
```

## Option 2: 로컬 개발 환경

### 1. 백엔드 설정

```bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 필요한 값 설정

# 마이그레이션
cd src
python manage.py migrate

# 샘플 데이터 생성 (선택)
python manage.py create_sample_data

# 영어 교육 코스 생성 (선택)
python manage.py create_english_courses

# 모든 코스에 상세 모듈 추가 (선택)
python manage.py add_detailed_modules

# 슈퍼유저 생성
python manage.py createsuperuser

# 서버 실행
python manage.py runserver
```

### 2. Redis & Celery 실행

```bash
# 새 터미널: Redis
redis-server

# 새 터미널: Celery Worker
cd backend/src
celery -A config worker -l info

# 새 터미널: Celery Beat
celery -A config beat -l info
```

### 3. 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env.local
# .env.local 파일을 열어 필요한 값 설정

# 개발 서버 실행
npm run dev
```

## 필수 환경 변수

### Backend (.env)

```bash
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379/0
ANTHROPIC_API_KEY=your-anthropic-key  # 필수!
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 다음 단계

1. **API 키 설정**
   - Anthropic API 키 발급: https://console.anthropic.com/
   - `.env` 파일에 추가

2. **첫 코스 만들기**
   - 강사 계정으로 로그인
   - `/instructor/dashboard`로 이동
   - "새 코스 만들기" 클릭

3. **AI 튜터 테스트**
   - `/ai-tutor`로 이동
   - 질문 입력 및 대화

4. **문서 읽기**
   - [개발 가이드](docs/DEVELOPMENT.md)
   - [API 문서](docs/API.md)
   - [배포 가이드](docs/DEPLOYMENT.md)

## 문제 해결

### Docker 컨테이너가 시작되지 않음

```bash
# 로그 확인
docker-compose logs

# 컨테이너 재시작
docker-compose restart

# 완전히 재시작
docker-compose down
docker-compose up -d
```

### 마이그레이션 오류

```bash
# 마이그레이션 리셋
docker-compose exec backend python manage.py migrate --run-syncdb
```

### 포트 충돌

`.env` 파일에서 포트 변경:
- Frontend: `3000` → 다른 포트
- Backend: `8000` → 다른 포트

## 유용한 명령어

```bash
# Docker 서비스 상태 확인
docker-compose ps

# 로그 보기
docker-compose logs -f

# 특정 서비스 로그
docker-compose logs -f backend

# 서비스 재시작
docker-compose restart backend

# 데이터베이스 접속
docker-compose exec postgres psql -U education_user education_db

# Django 쉘
docker-compose exec backend python manage.py shell

# 테스트 실행
docker-compose exec backend pytest

# 프론트엔드 테스트
cd frontend && npm run test

# 영어 교육 코스 생성
docker-compose exec backend python manage.py create_english_courses

# 상세 모듈 추가 (일반 모듈을 구체적인 내용으로 대체)
docker-compose exec backend python manage.py add_detailed_modules

# 50개 추가 코스 생성 (Rust, Kotlin, Swift, 클라우드, 게임, 창작, 금융 등)
docker-compose exec backend python manage.py create_50_more_courses

# 각 코스에 50개 모듈 추가 (초급-중급-고급 상세 커리큘럼)
docker-compose exec backend python manage.py add_50_modules_per_course

# 또는 Makefile 사용
make english-courses
make detailed-modules
make create-50-more
make add-50-modules
```

## 지원

- 문제 리포트: GitHub Issues
- 문서: `/docs` 디렉토리
- 이메일: support@example.com
