"""
Management command to create 15 Chinese language education courses
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
from ai.models import PracticeQuestion
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create 15 Chinese language education courses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating 15 Chinese language courses...')

        # Get or create instructor
        instructor, created = User.objects.get_or_create(
            username='chinese_teacher',
            defaults={
                'email': 'chinese@example.com',
                'user_type': 'instructor',
                'first_name': '王',
                'last_name': '老师',
                'verified_instructor': True
            }
        )
        if created:
            instructor.set_password('instructor123')
            instructor.save()

        courses_data = [
            # HSK 시험 대비 (1-6)
            {
                'title': 'HSK 1급 완벽 대비',
                'slug': 'hsk-1-complete',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': 'HSK 1급 합격 보장',
                'description': 'HSK 1급 시험을 체계적으로 준비합니다. 150개 필수 어휘와 기초 문법을 마스터합니다.',
                'objectives': ['필수 어휘 150개', '기초 문법', '듣기 전략', '읽기 전략'],
                'duration_hours': 25,
                'enrollments': 4580,
                'rating': 4.8,
            },
            {
                'title': 'HSK 2급 완성',
                'slug': 'hsk-2-complete',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 79000,
                'short_description': 'HSK 2급 한 번에 합격',
                'description': 'HSK 2급 필수 어휘 300개와 기본 문법을 학습합니다.',
                'objectives': ['필수 어휘 300개', '기본 문법', '실전 문제', '모의고사'],
                'duration_hours': 30,
                'enrollments': 3920,
                'rating': 4.7,
            },
            {
                'title': 'HSK 3급 고득점 전략',
                'slug': 'hsk-3-high-score',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 99000,
                'short_description': 'HSK 3급 완벽 대비',
                'description': 'HSK 3급 600개 어휘와 중급 문법을 마스터합니다.',
                'objectives': ['필수 어휘 600개', '중급 문법', '듣기/독해/쓰기', '모의고사 5회'],
                'duration_hours': 40,
                'enrollments': 3240,
                'rating': 4.8,
            },
            {
                'title': 'HSK 4급 완전 정복',
                'slug': 'hsk-4-master',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 119000,
                'short_description': 'HSK 4급 합격의 지름길',
                'description': 'HSK 4급 1200개 어휘와 고급 문법을 체계적으로 학습합니다.',
                'objectives': ['필수 어휘 1200개', '고급 문법', '듣기/독해/쓰기', '실전 모의고사'],
                'duration_hours': 50,
                'enrollments': 2650,
                'rating': 4.7,
            },
            {
                'title': 'HSK 5급 완벽 대비',
                'slug': 'hsk-5-complete',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 149000,
                'short_description': 'HSK 5급 고득점 달성',
                'description': 'HSK 5급 2500개 어휘와 복잡한 문법 구조를 마스터합니다.',
                'objectives': ['필수 어휘 2500개', '복합 문법', '듣기/독해/쓰기', '모의고사 8회'],
                'duration_hours': 60,
                'enrollments': 1840,
                'rating': 4.9,
            },
            {
                'title': 'HSK 6급 최고 등급 달성',
                'slug': 'hsk-6-top-grade',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 179000,
                'short_description': 'HSK 6급 완전 정복',
                'description': 'HSK 최고 등급인 6급을 완벽하게 대비합니다. 5000개 이상의 어휘와 고급 표현을 학습합니다.',
                'objectives': ['필수 어휘 5000개', '고급 문법', '학술 중국어', '모의고사 10회'],
                'duration_hours': 70,
                'enrollments': 980,
                'rating': 4.8,
            },

            # 실용 중국어 (7-11)
            {
                'title': '왕초보 중국어 - 병음부터',
                'slug': 'chinese-beginner-pinyin',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '병음부터 시작하는 중국어',
                'description': '중국어를 전혀 모르는 초보자를 위한 과정입니다. 병음과 성조부터 차근차근 배웁니다.',
                'objectives': ['병음 마스터', '성조 4개', '기본 한자 100개', '자기소개'],
                'duration_hours': 20,
                'enrollments': 5680,
                'rating': 4.7,
            },
            {
                'title': '중국어 회화 첫걸음',
                'slug': 'chinese-conversation-basic',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '실생활 중국어 회화',
                'description': '일상생활에서 자주 쓰는 중국어 회화 표현을 배웁니다.',
                'objectives': ['인사', '쇼핑', '식당', '호텔', '교통'],
                'duration_hours': 25,
                'enrollments': 4250,
                'rating': 4.6,
            },
            {
                'title': '비즈니스 중국어 마스터',
                'slug': 'business-chinese-master',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 129000,
                'short_description': '직장에서 쓰는 중국어',
                'description': '비즈니스 현장에서 필요한 중국어를 학습합니다. 이메일, 회의, 협상 표현을 마스터합니다.',
                'objectives': ['이메일 작성', '회의 중국어', '협상', '프레젠테이션'],
                'duration_hours': 40,
                'enrollments': 2340,
                'rating': 4.8,
            },
            {
                'title': '여행 중국어 완벽 가이드',
                'slug': 'travel-chinese-complete',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 59000,
                'short_description': '중국 여행 필수 표현',
                'description': '중국 여행 시 필요한 모든 중국어 표현을 배웁니다.',
                'objectives': ['공항', '호텔', '식당', '쇼핑', '관광지'],
                'duration_hours': 15,
                'enrollments': 6840,
                'rating': 4.5,
            },
            {
                'title': '중국어 발음 교정',
                'slug': 'chinese-pronunciation-correction',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 69000,
                'short_description': '정확한 중국어 발음',
                'description': '중국어의 어려운 성조와 발음을 완벽하게 교정합니다.',
                'objectives': ['4성 마스터', '권설음', '경성', '억양'],
                'duration_hours': 18,
                'enrollments': 3150,
                'rating': 4.7,
            },

            # 심화 과정 (12-15)
            {
                'title': '중국어 한자 쓰기 마스터',
                'slug': 'chinese-character-writing',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '한자 쓰기 완전 정복',
                'description': '중국어 간체자를 올바른 필순으로 쓰는 법을 배웁니다. 1000자 쓰기를 마스터합니다.',
                'objectives': ['필순 규칙', '부수 214개', '상용 한자 1000자', '서예 기초'],
                'duration_hours': 35,
                'enrollments': 1840,
                'rating': 4.6,
            },
            {
                'title': '중국 드라마로 배우는 중국어',
                'slug': 'chinese-with-drama',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '드라마로 재미있게 배우기',
                'description': '인기 중국 드라마를 통해 실생활 중국어와 문화를 학습합니다.',
                'objectives': ['일상 표현', '속어', '문화 이해', '듣기 향상'],
                'duration_hours': 30,
                'enrollments': 4580,
                'rating': 4.8,
            },
            {
                'title': '중국어 작문 실력 향상',
                'slug': 'chinese-writing-skills',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 109000,
                'short_description': '논리적인 중국어 글쓰기',
                'description': '중국어로 에세이, 이메일, 보고서를 작성하는 법을 배웁니다.',
                'objectives': ['문단 구성', '논리적 전개', '공식 문서', '학술 작문'],
                'duration_hours': 35,
                'enrollments': 1240,
                'rating': 4.5,
            },
            {
                'title': '중국 문화와 성어',
                'slug': 'chinese-culture-idioms',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '성어로 배우는 중국 문화',
                'description': '중국의 사자성어(成语)를 통해 중국 문화와 역사를 이해합니다.',
                'objectives': ['성어 200개', '유래', '사용법', '문화 배경'],
                'duration_hours': 28,
                'enrollments': 1650,
                'rating': 4.7,
            },
        ]

        created_count = 0
        for course_data in courses_data:
            if Course.objects.filter(slug=course_data['slug']).exists():
                self.stdout.write(f'  ⏭️  Skipping {course_data["slug"]}')
                continue

            # Extract fields
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

            # Create basic modules (will be expanded by add_50_modules command)
            module_titles = ['입문', '초급', '중급', '고급', '실전']
            for idx, title in enumerate(module_titles[:3]):
                module = Module.objects.create(
                    course=course,
                    title=title,
                    description=f'{title} 단계 학습',
                    order=idx
                )
                for les_idx in range(3):
                    Lesson.objects.create(
                        module=module,
                        title=f'{title} 레슨 {les_idx + 1}',
                        lesson_type='video',
                        content=f'{title} 단계의 학습 내용입니다.',
                        order=les_idx,
                        is_preview=(idx == 0 and les_idx == 0),
                        video_duration=random.randint(600, 1800)
                    )

            # Create practice questions
            for _ in range(5):
                PracticeQuestion.objects.create(
                    course=course,
                    topic='중국어',
                    difficulty=random.choice(['easy', 'medium', 'hard']),
                    question=f'{course.title}에 대한 연습 문제입니다.',
                    options=['선택지 1', '선택지 2', '선택지 3', '선택지 4'],
                    correct_answer='선택지 1',
                    explanation='정답에 대한 설명입니다.'
                )

            created_count += 1
            self.stdout.write(f'  ✅ [{created_count}/15] {course.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully created {created_count} Chinese courses!'
                f'\n📚 Categories:'
                f'\n   - HSK 시험 대비 (6개): HSK 1-6급'
                f'\n   - 실용 중국어 (5개): 왕초보, 회화, 비즈니스, 여행, 발음'
                f'\n   - 심화 과정 (4개): 한자 쓰기, 드라마, 작문, 문화/성어'
            )
        )
