# 학습 프로그램 데이터 로드하기

이 가이드는 Money Education Platform에 100개의 학습 프로그램(코스)을 추가하는 방법을 설명합니다.

## 📊 포함된 데이터

- **코스**: 100개
  - 금융 (20개)
  - 프로그래밍 (20개)
  - 데이터 사이언스 (20개)
  - 비즈니스 (20개)
  - 마케팅 (20개)

- **강사**: 15명
- **모듈**: 약 1,250개 (각 코스당 10-15개)
- **레슨**: 약 12,500개 (각 모듈당 8-12개, 비디오/텍스트/퀴즈/과제)

## 🚀 방법 1: Fixtures 파일 사용 (권장)

가장 간단하고 빠른 방법입니다.

### 1. 데이터베이스 마이그레이션 실행

```bash
cd backend
python manage.py migrate
```

### 2. Fixtures 데이터 로드

```bash
python manage.py loaddata src/courses/fixtures/courses_fixtures.json
```

### 3. 확인

Django Admin 또는 API를 통해 데이터가 로드되었는지 확인합니다:

```bash
python manage.py shell
>>> from courses.models import Course
>>> Course.objects.count()
50
```

## 🔧 방법 2: Management Command 사용

커스터마이징이 필요한 경우 management command를 사용할 수 있습니다.

### 1. Management Command 실행

```bash
cd backend
python manage.py seed_courses
```

이 명령은 다음을 수행합니다:
- 8명의 강사 계정 생성
- 50개의 코스 생성 (각각 고유한 slug, 가격, 난이도 등)
- 각 코스당 3-6개의 모듈 생성
- 각 모듈당 4-8개의 레슨 생성

## 📝 코스 카테고리

### 금융 (finance)
- 주식 투자, 부동산, 암호화폐, 재무제표, 퀀트 투자 등

### 프로그래밍 (programming)
- Python, JavaScript, React, Node.js, Django, Docker, AWS 등

### 데이터 사이언스 (data_science)
- 데이터 분석, 머신러닝, 딥러닝, NLP, 시각화 등

### 비즈니스 (business)
- 스타트업, 린 스타트업, 프로젝트 관리, 협상, 세일즈 등

### 마케팅 (marketing)
- 디지털 마케팅, SEO, SNS 마케팅, 브랜딩, Growth Hacking 등

## 🎓 코스 난이도

- **beginner**: 초급 - 입문자를 위한 코스
- **intermediate**: 중급 - 기본 지식이 있는 학습자
- **advanced**: 고급 - 전문가 레벨 코스

## 💰 가격 정보

- 코스 가격: 29,000원 ~ 179,000원
- 30%의 코스에 할인가 적용 (정가의 70%)
- 모든 코스는 유료 (price_type: 'paid')

## 🔄 데이터 재생성

### Fixtures 파일 재생성

```bash
cd backend
python generate_fixtures.py
```

새로운 `courses_fixtures.json` 파일이 생성됩니다.

### 기존 데이터 삭제 후 재로드

```bash
# Django shell에서
python manage.py shell
>>> from courses.models import Course, Module, Lesson
>>> Lesson.objects.all().delete()
>>> Module.objects.all().delete()
>>> Course.objects.all().delete()
>>> exit()

# 데이터 재로드
python manage.py loaddata src/courses/fixtures/courses_fixtures.json
```

## 🐳 Docker 환경에서 실행

```bash
# Docker Compose로 서비스 시작
docker-compose up -d

# Backend 컨테이너에 접속
docker-compose exec backend bash

# Fixtures 로드
python manage.py loaddata src/courses/fixtures/courses_fixtures.json
```

## ⚠️ 주의사항

1. **User 모델**: Fixtures에는 강사(instructor) 유저만 포함됩니다. 학생 계정은 별도로 생성하세요.

2. **비밀번호**: Fixtures의 유저는 비밀번호가 설정되지 않습니다. Management command를 사용하면 기본 비밀번호(`password123`)가 설정됩니다.

3. **이미지/비디오**: 실제 이미지나 비디오 파일은 포함되지 않습니다. `thumbnail`과 `video_url` 필드에는 예시 URL이 들어갑니다.

4. **중복 데이터**: 동일한 fixtures를 여러 번 로드하면 중복 데이터가 생성될 수 있습니다. 기존 데이터를 먼저 삭제하세요.

## 🔍 API로 확인하기

서버 실행 후 API를 통해 데이터를 확인할 수 있습니다:

```bash
# 서버 시작
python manage.py runserver

# 브라우저에서 확인
http://localhost:8000/api/courses/
```

## 📚 추가 리소스

- Django Fixtures 공식 문서: https://docs.djangoproject.com/en/4.2/howto/initial-data/
- Django Management Commands: https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/
