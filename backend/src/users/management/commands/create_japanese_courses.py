"""
Management command to create 15 Japanese language education courses
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
from ai.models import PracticeQuestion
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create 15 Japanese language education courses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating 15 Japanese language courses...')

        # Get or create instructor
        instructor, created = User.objects.get_or_create(
            username='japanese_teacher',
            defaults={
                'email': 'japanese@example.com',
                'user_type': 'instructor',
                'first_name': 'Tanaka',
                'last_name': 'Sensei',
                'verified_instructor': True
            }
        )
        if created:
            instructor.set_password('instructor123')
            instructor.save()

        courses_data = [
            # JLPT 시험 대비 (1-5)
            {
                'title': 'JLPT N5 완벽 대비',
                'slug': 'jlpt-n5-complete',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': 'JLPT N5 합격 보장',
                'description': 'JLPT N5 시험을 체계적으로 준비합니다. 히라가나, 가타카나부터 기초 문법까지 완벽하게 학습합니다.',
                'objectives': ['히라가나/가타카나', '한자 100자', '기초 문법', '듣기/독해'],
                'duration_hours': 30,
                'enrollments': 6240,
                'rating': 4.8,
            },
            {
                'title': 'JLPT N4 한 번에 합격',
                'slug': 'jlpt-n4-pass',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 89000,
                'short_description': 'JLPT N4 완전 정복',
                'description': 'JLPT N4 필수 문법과 어휘를 마스터합니다.',
                'objectives': ['한자 300자', 'N4 문법', '어휘 1500개', '모의고사'],
                'duration_hours': 35,
                'enrollments': 4580,
                'rating': 4.7,
            },
            {
                'title': 'JLPT N3 완성',
                'slug': 'jlpt-n3-complete',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 109000,
                'short_description': 'JLPT N3 고득점 전략',
                'description': 'JLPT N3 중급 문법과 한자를 체계적으로 학습합니다.',
                'objectives': ['한자 600자', 'N3 문법', '어휘 3000개', '실전 연습'],
                'duration_hours': 45,
                'enrollments': 3420,
                'rating': 4.8,
            },
            {
                'title': 'JLPT N2 완벽 마스터',
                'slug': 'jlpt-n2-master',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 129000,
                'short_description': 'JLPT N2 한 번에 합격',
                'description': 'JLPT N2 고급 문법과 한자 1000자를 마스터합니다.',
                'objectives': ['한자 1000자', 'N2 문법', '어휘 6000개', '모의고사 10회'],
                'duration_hours': 55,
                'enrollments': 2840,
                'rating': 4.9,
            },
            {
                'title': 'JLPT N1 최고 등급 달성',
                'slug': 'jlpt-n1-top-grade',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 159000,
                'short_description': 'JLPT N1 완전 정복',
                'description': 'JLPT 최고 등급인 N1을 완벽하게 대비합니다. 한자 2000자와 고급 표현을 학습합니다.',
                'objectives': ['한자 2000자', 'N1 문법', '어휘 10000개', '실전 모의고사'],
                'duration_hours': 65,
                'enrollments': 1540,
                'rating': 4.8,
            },

            # 기초 과정 (6-10)
            {
                'title': '왕초보 일본어 - 히라가나부터',
                'slug': 'japanese-beginner-hiragana',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '히라가나/가타카나 완전 정복',
                'description': '일본어를 전혀 모르는 초보자를 위한 과정입니다. 히라가나와 가타카나부터 시작합니다.',
                'objectives': ['히라가나 46자', '가타카나 46자', '기본 인사', '자기소개'],
                'duration_hours': 15,
                'enrollments': 7840,
                'rating': 4.7,
            },
            {
                'title': '일본어 기초 문법',
                'slug': 'japanese-basic-grammar',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '일본어 문법 기초 완성',
                'description': '일본어의 기본 문법을 체계적으로 학습합니다. 조사, 동사 활용, 형용사를 마스터합니다.',
                'objectives': ['조사', '동사 3그룹', '형용사', '기본 문형'],
                'duration_hours': 30,
                'enrollments': 5240,
                'rating': 4.6,
            },
            {
                'title': '일본어 회화 첫걸음',
                'slug': 'japanese-conversation-basic',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '실생활 일본어 회화',
                'description': '일상생활에서 자주 쓰는 일본어 표현을 배웁니다.',
                'objectives': ['인사', '쇼핑', '식당', '교통', '전화'],
                'duration_hours': 25,
                'enrollments': 4650,
                'rating': 4.7,
            },
            {
                'title': '일본어 한자 마스터',
                'slug': 'japanese-kanji-master',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '일본 한자 1000자 정복',
                'description': '일본어 상용 한자 1000자를 읽기와 뜻을 학습합니다.',
                'objectives': ['상용 한자 1000자', '음독/훈독', '한자어', '필순'],
                'duration_hours': 40,
                'enrollments': 2840,
                'rating': 4.5,
            },
            {
                'title': '일본어 발음 교정',
                'slug': 'japanese-pronunciation-correction',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 59000,
                'short_description': '정확한 일본어 발음',
                'description': '일본어의 정확한 발음과 억양을 익힙니다.',
                'objectives': ['청음/탁음', '장음', '촉음', '억양'],
                'duration_hours': 18,
                'enrollments': 3250,
                'rating': 4.6,
            },

            # 심화 과정 (11-15)
            {
                'title': '비즈니스 일본어',
                'slug': 'business-japanese',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 129000,
                'short_description': '직장에서 쓰는 일본어',
                'description': '일본 회사에서 업무를 보기 위한 비즈니스 일본어를 학습합니다.',
                'objectives': ['경어', '이메일', '전화', '회의', '보고'],
                'duration_hours': 45,
                'enrollments': 2140,
                'rating': 4.8,
            },
            {
                'title': '여행 일본어 완벽 가이드',
                'slug': 'travel-japanese-complete',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 49000,
                'short_description': '일본 여행 필수 표현',
                'description': '일본 여행 시 필요한 모든 일본어 표현을 배웁니다.',
                'objectives': ['공항', '호텔', '식당', '쇼핑', '관광지'],
                'duration_hours': 12,
                'enrollments': 8540,
                'rating': 4.5,
            },
            {
                'title': '일본 애니메이션으로 배우는 일본어',
                'slug': 'japanese-with-anime',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '애니메이션으로 재미있게',
                'description': '인기 일본 애니메이션을 통해 일본어와 문화를 학습합니다.',
                'objectives': ['일상 표현', '슬랭', '문화', '듣기 향상'],
                'duration_hours': 30,
                'enrollments': 6240,
                'rating': 4.9,
            },
            {
                'title': '일본어 작문 실력 향상',
                'slug': 'japanese-writing-skills',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '논리적인 일본어 글쓰기',
                'description': '일본어로 에세이, 이메일, 보고서를 작성하는 법을 배웁니다.',
                'objectives': ['문단 구성', '경어', '공식 문서', '학술 작문'],
                'duration_hours': 35,
                'enrollments': 1640,
                'rating': 4.6,
            },
            {
                'title': '일본 문화와 속담',
                'slug': 'japanese-culture-proverbs',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '속담으로 배우는 일본 문화',
                'description': '일본의 속담과 관용구를 통해 일본 문화를 이해합니다.',
                'objectives': ['속담 100개', '관용구', '사자숙어', '문화 배경'],
                'duration_hours': 25,
                'enrollments': 1840,
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

            # Create basic modules
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
                    topic='일본어',
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
                f'\n✅ Successfully created {created_count} Japanese courses!'
                f'\n📚 Categories:'
                f'\n   - JLPT 시험 대비 (5개): N5, N4, N3, N2, N1'
                f'\n   - 기초 과정 (5개): 히라가나, 기초문법, 회화, 한자, 발음'
                f'\n   - 심화 과정 (5개): 비즈니스, 여행, 애니메이션, 작문, 문화'
            )
        )
