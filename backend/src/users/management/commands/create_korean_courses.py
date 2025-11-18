"""
Management command to create 20 Korean language education courses
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
from ai.models import PracticeQuestion
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create 20 Korean language education courses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating 20 Korean language courses...')

        # Get or create instructor
        instructor, created = User.objects.get_or_create(
            username='korean_teacher',
            defaults={
                'email': 'korean@example.com',
                'user_type': 'instructor',
                'first_name': '김',
                'last_name': '선생님',
                'verified_instructor': True
            }
        )
        if created:
            instructor.set_password('instructor123')
            instructor.save()

        courses_data = [
            # 초급 과정 (1-5)
            {
                'title': '한국어 첫걸음 - 한글부터 기초 회화까지',
                'slug': 'korean-beginner-hangeul',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '한글 자모음부터 시작하는 한국어',
                'description': '한글을 전혀 모르는 외국인을 위한 왕초보 한국어 과정입니다. 자음과 모음부터 차근차근 배웁니다.',
                'objectives': ['한글 읽기/쓰기', '기본 인사', '자기소개', '숫자와 날짜'],
                'duration_hours': 20,
                'enrollments': 5240,
                'rating': 4.9,
                'modules': [
                    {
                        'title': '한글의 기초',
                        'lessons': ['한글의 원리', '자음 14개', '모음 10개', '받침', '한글 읽기 연습']
                    },
                    {
                        'title': '기본 인사와 표현',
                        'lessons': ['안녕하세요', '감사합니다/죄송합니다', '네/아니요', '이름 묻기', '국적 말하기']
                    },
                    {
                        'title': '숫자와 시간',
                        'lessons': ['고유어 숫자', '한자어 숫자', '날짜', '시간', '나이']
                    },
                    {
                        'title': '일상 회화 기초',
                        'lessons': ['가족 소개', '취미 이야기', '좋아하는 것', '간단한 질문', '기초 대화']
                    }
                ],
                'practice_questions': [
                    {'question': '한글 자음은 몇 개인가요?', 'correct_answer': '14개', 'difficulty': 'easy'},
                    {'question': '"안녕하세요"는 언제 사용하나요?', 'correct_answer': '처음 만날 때 인사', 'difficulty': 'easy'},
                ]
            },
            {
                'title': '한국어 기초 문법 완성',
                'slug': 'korean-basic-grammar',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '한국어 기초 문법 총정리',
                'description': '한국어의 기본 문법을 체계적으로 학습합니다. 조사, 어미, 시제 등을 완벽하게 익힙니다.',
                'objectives': ['조사 사용법', '시제 표현', '존댓말', '기본 문형'],
                'duration_hours': 30,
                'enrollments': 3820,
                'rating': 4.7,
                'modules': [
                    {'title': '조사 마스터', 'lessons': ['은/는', '이/가', '을/를', '에/에서', '의', '와/과']},
                    {'title': '동사와 형용사', 'lessons': ['기본형', '현재형', '과거형', '미래형', '부정형']},
                    {'title': '존댓말과 반말', 'lessons': ['해요체', '합니다체', '반말', '높임말', '상황별 사용']},
                    {'title': '기본 문형', 'lessons': ['-고 싶다', '-을 수 있다', '-어야 하다', '-지 마세요', '-으면']}
                ],
                'practice_questions': [
                    {'question': '"학교에 가요"와 "학교에서 공부해요"의 차이는?', 'correct_answer': '에는 목적지, 에서는 장소', 'difficulty': 'medium'},
                ]
            },
            {
                'title': '한국어 일상 회화 마스터',
                'slug': 'korean-daily-conversation',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '실생활 한국어 회화',
                'description': '일상생활에서 자주 쓰는 한국어 표현을 배웁니다. 쇼핑, 식당, 교통 등 다양한 상황을 다룹니다.',
                'objectives': ['쇼핑 회화', '식당 주문', '길 묻기', '전화 통화'],
                'duration_hours': 25,
                'enrollments': 4150,
                'rating': 4.8,
            },
            {
                'title': '한국어 발음 교정 완벽 가이드',
                'slug': 'korean-pronunciation-perfect',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 69000,
                'short_description': '정확한 한국어 발음',
                'description': '한국어의 어려운 발음을 교정합니다. 격음, 경음, 받침 발음을 완벽하게 익힙니다.',
                'objectives': ['자음 정확한 발음', '받침 발음', '연음 규칙', '억양'],
                'duration_hours': 15,
                'enrollments': 2840,
                'rating': 4.6,
            },
            {
                'title': '한국어 듣기 집중 훈련',
                'slug': 'korean-listening-intensive',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '한국어 듣기 능력 향상',
                'description': '다양한 속도와 억양의 한국어를 듣고 이해하는 능력을 키웁니다.',
                'objectives': ['일상 대화 듣기', '뉴스 청취', '드라마 이해', '받아쓰기'],
                'duration_hours': 20,
                'enrollments': 3240,
                'rating': 4.7,
            },

            # 중급 과정 (6-10)
            {
                'title': 'TOPIK I (1-2급) 완벽 대비',
                'slug': 'topik-1-complete',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 129000,
                'short_description': 'TOPIK I 합격 보장',
                'description': 'TOPIK I 시험을 체계적으로 준비합니다. 듣기, 읽기 영역을 완벽하게 대비합니다.',
                'objectives': ['듣기 전략', '읽기 전략', '어휘 1000개', '실전 모의고사'],
                'duration_hours': 40,
                'enrollments': 4580,
                'rating': 4.8,
            },
            {
                'title': 'TOPIK II (3-6급) 고득점 전략',
                'slug': 'topik-2-high-score',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 159000,
                'short_description': 'TOPIK II 5-6급 목표',
                'description': 'TOPIK II에서 고득점을 받기 위한 전략을 학습합니다. 듣기, 읽기, 쓰기 모든 영역을 다룹니다.',
                'objectives': ['듣기 고급', '읽기 고급', '쓰기 51-54번', '모의고사 10회'],
                'duration_hours': 50,
                'enrollments': 3920,
                'rating': 4.9,
            },
            {
                'title': '한국어 중급 문법',
                'slug': 'korean-intermediate-grammar',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '중급 문법 완성',
                'description': '한국어 중급 문법을 체계적으로 학습합니다. 연결어미, 간접화법 등을 마스터합니다.',
                'objectives': ['연결어미', '간접화법', '피동/사동', '관형사형'],
                'duration_hours': 35,
                'enrollments': 2650,
                'rating': 4.6,
            },
            {
                'title': '한국어 작문 실력 향상',
                'slug': 'korean-writing-skills',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '논리적인 한국어 글쓰기',
                'description': '한국어로 에세이, 이메일, 보고서를 작성하는 법을 배웁니다.',
                'objectives': ['문단 구성', '논리적 전개', '공식 문서', '창작 글쓰기'],
                'duration_hours': 30,
                'enrollments': 1980,
                'rating': 4.5,
            },
            {
                'title': '비즈니스 한국어',
                'slug': 'business-korean',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 119000,
                'short_description': '직장에서 쓰는 한국어',
                'description': '한국 회사에서 업무를 보기 위한 비즈니스 한국어를 학습합니다.',
                'objectives': ['이메일 작성', '회의 한국어', '전화 응대', '보고서'],
                'duration_hours': 40,
                'enrollments': 2340,
                'rating': 4.7,
            },

            # 고급 과정 (11-15)
            {
                'title': '한국 드라마로 배우는 한국어',
                'slug': 'korean-with-drama',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '드라마로 재미있게 배우기',
                'description': '인기 한국 드라마를 활용하여 실생활 한국어와 문화를 자연스럽게 학습합니다.',
                'objectives': ['일상 표현', '슬랭', '문화 이해', '듣기 향상'],
                'duration_hours': 30,
                'enrollments': 5680,
                'rating': 4.9,
            },
            {
                'title': 'K-POP으로 배우는 한국어',
                'slug': 'korean-with-kpop',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 69000,
                'short_description': 'K-POP 가사로 한국어 학습',
                'description': '좋아하는 K-POP 노래 가사를 통해 한국어를 즐겁게 배웁니다.',
                'objectives': ['가사 이해', '발음 연습', '문화', '노래하기'],
                'duration_hours': 20,
                'enrollments': 6240,
                'rating': 4.8,
            },
            {
                'title': '한국 문화와 관용어',
                'slug': 'korean-culture-idioms',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '속담과 관용 표현',
                'description': '한국인처럼 말하기 위한 속담, 관용어, 사자성어를 학습합니다.',
                'objectives': ['속담 100개', '관용어', '사자성어', '문화 배경'],
                'duration_hours': 25,
                'enrollments': 1850,
                'rating': 4.6,
            },
            {
                'title': '한국어 고급 문법',
                'slug': 'korean-advanced-grammar',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 109000,
                'short_description': '고급 문법 마스터',
                'description': '한국어의 복잡한 고급 문법을 완벽하게 이해합니다.',
                'objectives': ['고급 연결어미', '복합 표현', '문어체', '학술 한국어'],
                'duration_hours': 40,
                'enrollments': 1420,
                'rating': 4.7,
            },
            {
                'title': '한국어 토론과 발표',
                'slug': 'korean-debate-presentation',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 129000,
                'short_description': '논리적 말하기',
                'description': '한국어로 자신의 의견을 논리적으로 표현하고 발표하는 능력을 키웁니다.',
                'objectives': ['의견 제시', '논증', 'PT 기법', '토론'],
                'duration_hours': 35,
                'enrollments': 980,
                'rating': 4.5,
            },

            # 특화 과정 (16-20)
            {
                'title': '한국어 한자 마스터',
                'slug': 'korean-hanja-master',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '한국어 속 한자 완전 정복',
                'description': '한국어에서 자주 쓰이는 한자 1000자를 학습합니다.',
                'objectives': ['기초 한자 500', '중급 한자 500', '한자어', '사자성어'],
                'duration_hours': 30,
                'enrollments': 1240,
                'rating': 4.4,
            },
            {
                'title': '한국어 뉴스 읽기',
                'slug': 'korean-news-reading',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '시사 한국어 마스터',
                'description': '한국 뉴스를 읽고 이해하며 시사 어휘를 확장합니다.',
                'objectives': ['뉴스 어휘', '정치/경제/사회', '뉴스 청취', '요약'],
                'duration_hours': 25,
                'enrollments': 1580,
                'rating': 4.6,
            },
            {
                'title': '여행 한국어 완벽 가이드',
                'slug': 'travel-korean-complete',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '한국 여행 필수 표현',
                'description': '한국 여행 시 필요한 모든 한국어 표현을 배웁니다.',
                'objectives': ['공항', '호텔', '식당', '쇼핑', '관광지'],
                'duration_hours': 12,
                'enrollments': 7840,
                'rating': 4.7,
            },
            {
                'title': '한국어 동화 읽기',
                'slug': 'korean-fairy-tales',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 59000,
                'short_description': '동화로 배우는 한국어',
                'description': '한국 전래동화와 창작동화를 읽으며 재미있게 한국어를 배웁니다.',
                'objectives': ['전래동화 10편', '어휘 확장', '읽기 유창성', '문화'],
                'duration_hours': 18,
                'enrollments': 2450,
                'rating': 4.8,
            },
            {
                'title': '한국어 교사 자격증 대비',
                'slug': 'korean-teacher-certification',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 199000,
                'short_description': '한국어 교원 자격증',
                'description': '한국어 교원 자격증 시험을 준비하고 교수법을 학습합니다.',
                'objectives': ['한국어학', '한국어 교육론', '한국 문화', '교수법'],
                'duration_hours': 60,
                'enrollments': 840,
                'rating': 4.9,
            },
        ]

        created_count = 0
        for course_data in courses_data:
            if Course.objects.filter(slug=course_data['slug']).exists():
                self.stdout.write(f'  ⏭️  Skipping {course_data["slug"]}')
                continue

            # Extract fields
            modules_data = course_data.pop('modules', [])
            practice_questions = course_data.pop('practice_questions', [])
            objectives = course_data.pop('objectives')
            price = course_data.pop('price', 0)
            duration = course_data.pop('duration_hours', 20)
            enrollments = course_data.pop('enrollments', 1000)
            rating = course_data.pop('rating', 4.5)

            # Create course
            course = Course.objects.create(
                instructor=instructor,
                price=price,
                is_published=True,
                total_enrollments=enrollments,
                average_rating=rating,
                rating_count=random.randint(50, 1000),
                total_duration_minutes=duration * 60,
                **course_data
            )
            course.learning_objectives = objectives
            course.save()

            # Create modules and lessons
            for idx, module_data in enumerate(modules_data):
                lessons_data = module_data.pop('lessons', [])
                module = Module.objects.create(
                    course=course,
                    title=module_data['title'],
                    description=f"{module_data['title']} 학습 내용",
                    order=idx
                )

                for les_idx, lesson_title in enumerate(lessons_data):
                    lesson_type = random.choice(['video', 'video', 'video', 'text', 'quiz'])
                    Lesson.objects.create(
                        module=module,
                        title=lesson_title,
                        lesson_type=lesson_type,
                        content=f'{lesson_title} 학습 내용입니다.',
                        order=les_idx,
                        is_preview=(idx == 0 and les_idx == 0),
                        video_duration=random.randint(600, 2400) if lesson_type == 'video' else 0
                    )

            # Create practice questions
            for q_data in practice_questions:
                PracticeQuestion.objects.create(
                    course=course,
                    topic='한국어',
                    difficulty=q_data.get('difficulty', 'medium'),
                    question=q_data['question'],
                    options=[q_data['correct_answer'], '오답 1', '오답 2', '오답 3'],
                    correct_answer=q_data['correct_answer'],
                    explanation=f"정답: {q_data['correct_answer']}"
                )

            created_count += 1
            self.stdout.write(f'  ✅ [{created_count}/20] {course.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully created {created_count} Korean courses!'
                f'\n📚 Categories:'
                f'\n   - 초급 과정 (5개): 한글, 기초문법, 일상회화, 발음, 듣기'
                f'\n   - 중급 과정 (5개): TOPIK I/II, 중급문법, 작문, 비즈니스'
                f'\n   - 고급 과정 (5개): 드라마, K-POP, 문화/관용어, 고급문법, 토론'
                f'\n   - 특화 과정 (5개): 한자, 뉴스, 여행, 동화, 교사자격증'
            )
        )
