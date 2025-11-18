"""
Management command to create sample data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
from ai.models import PracticeQuestion

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create users
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        if not User.objects.filter(username='instructor1').exists():
            instructor = User.objects.create_user(
                username='instructor1',
                email='instructor@example.com',
                password='instructor123',
                first_name='John',
                last_name='Doe',
                user_type='instructor',
                verified_instructor=True
            )
            self.stdout.write(self.style.SUCCESS('Created instructor user'))
        else:
            instructor = User.objects.get(username='instructor1')

        if not User.objects.filter(username='student1').exists():
            student = User.objects.create_user(
                username='student1',
                email='student@example.com',
                password='student123',
                first_name='Jane',
                last_name='Smith',
                user_type='student'
            )
            self.stdout.write(self.style.SUCCESS('Created student user'))

        # Create sample courses
        courses_data = [
            {
                'title': 'Python 완벽 가이드',
                'slug': 'python-complete-guide',
                'short_description': '초보자를 위한 Python 프로그래밍 완벽 가이드',
                'description': '''이 코스에서는 Python의 기초부터 고급 개념까지 모든 것을 배웁니다.

실습 위주로 진행되며, 실제 프로젝트를 만들면서 배웁니다.''',
                'category': 'programming',
                'difficulty': 'beginner',
                'price_type': 'free',
                'is_published': True,
                'learning_objectives': [
                    'Python 기본 문법 이해',
                    '객체지향 프로그래밍 개념 습득',
                    '실전 프로젝트 개발 능력',
                    '데이터 처리 및 분석 기초'
                ]
            },
            {
                'title': 'Django 웹 개발',
                'slug': 'django-web-development',
                'short_description': 'Django로 웹 애플리케이션 만들기',
                'description': 'Django 프레임워크를 이용한 풀스택 웹 개발을 배웁니다.',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 49000,
                'is_published': True,
                'learning_objectives': [
                    'Django 프레임워크 이해',
                    'REST API 개발',
                    '데이터베이스 설계',
                    '배포 및 운영'
                ]
            },
            {
                'title': '머신러닝 기초',
                'slug': 'machine-learning-basics',
                'short_description': '머신러닝의 기본 개념과 실습',
                'description': '머신러닝의 기초 개념부터 실전 프로젝트까지',
                'category': 'data-science',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 79000,
                'is_published': True,
                'learning_objectives': [
                    '머신러닝 기본 개념',
                    '주요 알고리즘 이해',
                    '실전 프로젝트 구현'
                ]
            }
        ]

        for course_data in courses_data:
            if not Course.objects.filter(slug=course_data['slug']).exists():
                objectives = course_data.pop('learning_objectives')
                course = Course.objects.create(
                    instructor=instructor,
                    **course_data
                )
                course.learning_objectives = objectives
                course.save()

                # Create modules and lessons
                module = Module.objects.create(
                    course=course,
                    title='시작하기',
                    description='코스 소개 및 환경 설정',
                    order=0
                )

                Lesson.objects.create(
                    module=module,
                    title='코스 소개',
                    lesson_type='video',
                    content='이 코스에서 무엇을 배우는지 알아봅니다.',
                    order=0,
                    is_preview=True
                )

                Lesson.objects.create(
                    module=module,
                    title='개발 환경 설정',
                    lesson_type='text',
                    content='필요한 도구들을 설치하고 환경을 설정합니다.',
                    order=1,
                    is_preview=True
                )

                # Create practice questions
                PracticeQuestion.objects.create(
                    course=course,
                    topic='Python 기초',
                    difficulty='easy',
                    question='Python에서 변수를 선언하는 방법은?',
                    options=['var x = 10', 'x = 10', 'int x = 10', 'let x = 10'],
                    correct_answer='x = 10',
                    explanation='Python에서는 타입 선언 없이 변수 이름과 값을 할당하면 됩니다.'
                )

                self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
