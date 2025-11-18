"""
Management command to add detailed modules to existing 50 courses
"""
from django.core.management.base import BaseCommand
from courses.models import Course, Module, Lesson
import random


class Command(BaseCommand):
    help = 'Add detailed modules and lessons to existing 50 courses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding detailed modules to courses...')

        # Module templates by category
        module_templates = {
            'programming': {
                'patterns': [
                    {
                        'title': '개발 환경 설정',
                        'lessons': ['IDE 설치 및 설정', '가상환경 구축', '버전 관리 시작하기', '디버깅 도구 활용']
                    },
                    {
                        'title': '핵심 문법과 개념',
                        'lessons': ['변수와 자료형', '제어문과 반복문', '함수와 모듈', '객체지향 프로그래밍', '에러 처리']
                    },
                    {
                        'title': '고급 기능',
                        'lessons': ['데코레이터와 제너레이터', '비동기 프로그래밍', '메타클래스', '타입 힌팅', '성능 최적화']
                    },
                    {
                        'title': '실전 프로젝트',
                        'lessons': ['프로젝트 설계', '코드 구현', '테스트 작성', '배포 준비', '유지보수 전략']
                    },
                    {
                        'title': '프레임워크 마스터',
                        'lessons': ['프레임워크 설치', '기본 구조 이해', 'CRUD 구현', 'API 개발', '인증과 권한']
                    },
                ],
            },
            'data_science': {
                'patterns': [
                    {
                        'title': '데이터 분석 기초',
                        'lessons': ['데이터 불러오기', '데이터 탐색', '결측치 처리', '이상치 탐지', '데이터 시각화']
                    },
                    {
                        'title': '통계와 수학',
                        'lessons': ['기술통계', '확률분포', '가설검정', '상관분석', '회귀분석']
                    },
                    {
                        'title': '머신러닝 모델',
                        'lessons': ['선형 회귀', '로지스틱 회귀', '의사결정 나무', '랜덤 포레스트', 'XGBoost', 'SVM']
                    },
                    {
                        'title': '딥러닝 기초',
                        'lessons': ['신경망 구조', '역전파 알고리즘', 'CNN', 'RNN/LSTM', 'Transformer']
                    },
                    {
                        'title': '모델 최적화와 배포',
                        'lessons': ['하이퍼파라미터 튜닝', '교차 검증', '모델 평가', '파이프라인 구축', 'API 서빙']
                    },
                ],
            },
            'design': {
                'patterns': [
                    {
                        'title': '디자인 기초',
                        'lessons': ['디자인 원칙', '색상 이론', '타이포그래피', '레이아웃 기법', '그리드 시스템']
                    },
                    {
                        'title': '툴 마스터',
                        'lessons': ['인터페이스 둘러보기', '핵심 도구 사용법', '레이어와 마스크', '단축키 활용', '플러그인 설정']
                    },
                    {
                        'title': 'UI/UX 디자인',
                        'lessons': ['사용자 리서치', '와이어프레임', '프로토타이핑', '유저 테스트', '피드백 반영']
                    },
                    {
                        'title': '실전 프로젝트',
                        'lessons': ['클라이언트 미팅', '컨셉 개발', '디자인 시안', '피드백 수정', '최종 파일 전달']
                    },
                    {
                        'title': '포트폴리오 제작',
                        'lessons': ['작품 선정', '케이스 스터디 작성', '포트폴리오 사이트', '프레젠테이션 기법', '취업 전략']
                    },
                ],
            },
            'marketing': {
                'patterns': [
                    {
                        'title': '마케팅 기초',
                        'lessons': ['마케팅 개념', '타겟 분석', '경쟁사 조사', '포지셔닝', 'USP 개발']
                    },
                    {
                        'title': '디지털 마케팅 전략',
                        'lessons': ['SEO 최적화', 'SEM 광고', 'SNS 마케팅', '콘텐츠 마케팅', '이메일 마케팅']
                    },
                    {
                        'title': '광고 캠페인 운영',
                        'lessons': ['캠페인 기획', '크리에이티브 제작', '예산 설정', '광고 집행', 'A/B 테스트']
                    },
                    {
                        'title': '데이터 분석',
                        'lessons': ['GA4 설정', '전환 추적', 'KPI 설정', '대시보드 구축', '보고서 작성']
                    },
                    {
                        'title': '수익화 전략',
                        'lessons': ['퍼널 최적화', 'CRO 기법', '리타게팅', '이메일 자동화', 'LTV 증대']
                    },
                ],
            },
            'language': {
                'patterns': [
                    {
                        'title': '기초 다지기',
                        'lessons': ['알파벳/발음', '기본 문법', '필수 어휘 100', '간단한 문장', '자기소개']
                    },
                    {
                        'title': '일상 회화',
                        'lessons': ['인사와 소개', '쇼핑과 주문', '길 묻기', '전화 통화', '약속 잡기']
                    },
                    {
                        'title': '문법 심화',
                        'lessons': ['시제 완벽 정리', '조동사', '가정법', '관계사', '분사구문']
                    },
                    {
                        'title': '실전 활용',
                        'lessons': ['비즈니스 회화', '프레젠테이션', '토론과 논쟁', '협상 영어', '이메일 작성']
                    },
                    {
                        'title': '시험 대비',
                        'lessons': ['듣기 전략', '독해 스킬', '말하기 연습', '쓰기 템플릿', '실전 모의고사']
                    },
                ],
            },
            'business': {
                'patterns': [
                    {
                        'title': '비즈니스 기초',
                        'lessons': ['경영의 이해', '재무제표 읽기', '손익분기점', '시장 분석', '사업 계획서']
                    },
                    {
                        'title': '실무 스킬',
                        'lessons': ['엑셀 고급 기능', '데이터 분석', '프레젠테이션', '문서 작성', '협업 도구']
                    },
                    {
                        'title': '프로젝트 관리',
                        'lessons': ['PM 기초', '일정 관리', '리스크 관리', '팀 커뮤니케이션', '성과 평가']
                    },
                    {
                        'title': '자동화',
                        'lessons': ['매크로 작성', 'VBA 프로그래밍', 'API 활용', '워크플로우 설계', '시간 절약 기법']
                    },
                    {
                        'title': '케이스 스터디',
                        'lessons': ['성공 사례 분석', '실패 사례 학습', '문제 해결', '의사결정', '전략 수립']
                    },
                ],
            },
        }

        # Get all courses
        courses = Course.objects.all().order_by('id')

        updated_count = 0
        total_modules_added = 0

        for course in courses:
            # Determine category for template
            category = course.category
            if category not in module_templates:
                if 'programming' in course.slug or 'python' in course.slug or 'java' in course.slug:
                    category = 'programming'
                elif 'data' in course.slug or 'ml' in course.slug or 'ai' in course.slug:
                    category = 'data_science'
                elif 'design' in course.slug or 'ui' in course.slug or 'figma' in course.slug:
                    category = 'design'
                elif 'marketing' in course.slug or 'seo' in course.slug or 'ads' in course.slug:
                    category = 'marketing'
                elif 'english' in course.slug or 'language' in course.slug or 'toeic' in course.slug:
                    category = 'language'
                else:
                    category = 'business'

            # Delete existing generic modules
            existing_modules = course.modules.all()
            generic_titles = ['시작하기', '기초 다지기', '핵심 개념', '실전 응용', '프로젝트']
            modules_deleted = 0

            for module in existing_modules:
                if module.title in generic_titles:
                    module.delete()
                    modules_deleted += 1

            # Get templates
            templates = module_templates.get(category, module_templates['business'])

            # Add detailed modules
            num_modules = random.randint(4, 5)  # 4-5 modules per course
            selected_templates = random.sample(templates['patterns'], min(num_modules, len(templates['patterns'])))

            for idx, template in enumerate(selected_templates):
                module = Module.objects.create(
                    course=course,
                    title=template['title'],
                    description=f"{template['title']}에 대한 상세한 학습 내용",
                    order=idx
                )
                total_modules_added += 1

                # Add lessons
                num_lessons = random.randint(4, min(6, len(template['lessons'])))
                selected_lessons = random.sample(template['lessons'], num_lessons)

                for les_idx, lesson_title in enumerate(selected_lessons):
                    lesson_types = ['video', 'video', 'video', 'text', 'quiz']  # More videos
                    lesson_type = random.choice(lesson_types)

                    Lesson.objects.create(
                        module=module,
                        title=lesson_title,
                        lesson_type=lesson_type,
                        content=f'{lesson_title}에 대한 상세한 학습 내용과 예제입니다.',
                        order=les_idx,
                        is_preview=(idx == 0 and les_idx == 0),  # First lesson of first module
                        video_duration=random.randint(600, 2400) if lesson_type == 'video' else 0
                    )

            updated_count += 1
            self.stdout.write(f'  ✅ [{updated_count}/{courses.count()}] {course.title} - {num_modules}개 모듈 추가')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully updated {updated_count} courses!'
                f'\n📦 Total modules added: {total_modules_added}'
                f'\n📚 Average modules per course: {total_modules_added/updated_count:.1f}'
            )
        )
