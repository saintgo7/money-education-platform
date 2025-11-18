"""
Management command to create 30 certification preparation courses
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
from ai.models import PracticeQuestion
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create 30 certification preparation courses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating 30 certification courses...')

        # Get existing instructors
        instructors = list(User.objects.filter(user_type='instructor'))
        if len(instructors) < 5:
            # Create a certification instructor
            cert_instructor = User.objects.create_user(
                username='cert_instructor',
                email='cert@example.com',
                password='instructor123',
                first_name='자격증',
                last_name='전문가',
                user_type='instructor',
                verified_instructor=True
            )
            instructors.append(cert_instructor)

        courses_data = [
            # IT 자격증 (1-12)
            {
                'title': '정보처리기사 필기 완벽 대비',
                'slug': 'engineer-information-processing-written',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 149000,
                'short_description': '정보처리기사 한 번에 합격',
                'description': '정보처리기사 필기 시험을 체계적으로 준비합니다. 5과목을 완벽하게 마스터합니다.',
                'objectives': ['소프트웨어 설계', '소프트웨어 개발', '데이터베이스 구축', '프로그래밍 언어 활용', '정보시스템 구축관리'],
                'duration_hours': 60,
                'enrollments': 4580,
                'rating': 4.8,
            },
            {
                'title': '정보처리기사 실기 완전 정복',
                'slug': 'engineer-information-processing-practical',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 129000,
                'short_description': '실기 시험 완벽 대비',
                'description': '정보처리기사 실기 시험의 SQL, 알고리즘, 개발 등 실무 문제를 완벽하게 준비합니다.',
                'objectives': ['SQL 작성', '알고리즘 구현', 'ERD 설계', '실전 모의고사'],
                'duration_hours': 50,
                'enrollments': 3920,
                'rating': 4.7,
            },
            {
                'title': 'AWS Certified Solutions Architect',
                'slug': 'aws-solutions-architect-cert',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 199000,
                'short_description': 'AWS SAA 자격증 취득',
                'description': 'AWS Solutions Architect Associate 자격증을 취득합니다.',
                'objectives': ['AWS 서비스', '아키텍처 설계', '보안', '비용 최적화'],
                'duration_hours': 70,
                'enrollments': 2840,
                'rating': 4.9,
            },
            {
                'title': 'Google Cloud Associate Cloud Engineer',
                'slug': 'gcp-associate-cloud-engineer',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 179000,
                'short_description': 'GCP ACE 자격증',
                'description': 'Google Cloud Associate Cloud Engineer 자격증을 준비합니다.',
                'objectives': ['GCP 서비스', '클라우드 솔루션', '리소스 관리', '네트워킹'],
                'duration_hours': 65,
                'enrollments': 1920,
                'rating': 4.7,
            },
            {
                'title': 'CompTIA A+ 완벽 대비',
                'slug': 'comptia-aplus-complete',
                'category': 'certification',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 149000,
                'short_description': 'IT 기초 자격증',
                'description': 'CompTIA A+ 자격증으로 IT 전문가의 첫 걸음을 시작합니다.',
                'objectives': ['하드웨어', '네트워킹', '모바일 디바이스', '운영체제', '보안'],
                'duration_hours': 55,
                'enrollments': 2340,
                'rating': 4.6,
            },
            {
                'title': 'CompTIA Security+ 보안 자격증',
                'slug': 'comptia-security-plus',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 169000,
                'short_description': '사이버 보안 전문가',
                'description': 'CompTIA Security+ 자격증으로 정보보안 전문가가 됩니다.',
                'objectives': ['보안 위협', '암호화', '네트워크 보안', '접근 제어', '위험 관리'],
                'duration_hours': 60,
                'enrollments': 1840,
                'rating': 4.8,
            },
            {
                'title': 'CCNA (Cisco Certified Network Associate)',
                'slug': 'ccna-cisco-network',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 189000,
                'short_description': 'Cisco 네트워크 자격증',
                'description': 'CCNA 자격증으로 네트워크 엔지니어의 길을 시작합니다.',
                'objectives': ['네트워크 기초', 'IP 주소', '라우팅', '스위칭', '보안'],
                'duration_hours': 65,
                'enrollments': 1540,
                'rating': 4.7,
            },
            {
                'title': 'CISSP (Certified Information Systems Security Professional)',
                'slug': 'cissp-security-professional',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 249000,
                'short_description': '최고 수준 보안 자격증',
                'description': '정보보안 최고 자격증인 CISSP를 취득합니다.',
                'objectives': ['보안 위험 관리', '자산 보안', '보안 아키텍처', '통신 보안', '신원 관리'],
                'duration_hours': 80,
                'enrollments': 840,
                'rating': 4.9,
            },
            {
                'title': 'PMP (Project Management Professional)',
                'slug': 'pmp-project-management',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 229000,
                'short_description': '프로젝트 관리 전문가',
                'description': 'PMP 자격증으로 프로젝트 관리 전문가가 됩니다.',
                'objectives': ['프로젝트 시작', '계획', '실행', '감시 및 통제', '종료'],
                'duration_hours': 75,
                'enrollments': 1240,
                'rating': 4.8,
            },
            {
                'title': 'CKA (Certified Kubernetes Administrator)',
                'slug': 'cka-kubernetes-admin',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 199000,
                'short_description': 'Kubernetes 관리자',
                'description': 'CKA 자격증으로 Kubernetes 전문가가 됩니다.',
                'objectives': ['클러스터 아키텍처', '워크로드', '스케줄링', '서비스', '스토리지', '보안'],
                'duration_hours': 70,
                'enrollments': 980,
                'rating': 4.9,
            },
            {
                'title': 'CKAD (Certified Kubernetes Application Developer)',
                'slug': 'ckad-kubernetes-developer',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 189000,
                'short_description': 'Kubernetes 개발자',
                'description': 'CKAD 자격증으로 Kubernetes 애플리케이션 개발 전문가가 됩니다.',
                'objectives': ['컨테이너 설계', '멀티 컨테이너 Pod', '관찰 가능성', 'Pod 디자인', '서비스'],
                'duration_hours': 65,
                'enrollments': 840,
                'rating': 4.8,
            },
            {
                'title': 'RHCSA (Red Hat Certified System Administrator)',
                'slug': 'rhcsa-redhat-sysadmin',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 179000,
                'short_description': 'Red Hat 시스템 관리자',
                'description': 'RHCSA 자격증으로 Linux 시스템 관리 전문가가 됩니다.',
                'objectives': ['시스템 관리', '파일 시스템', '사용자 관리', '네트워크', '보안'],
                'duration_hours': 60,
                'enrollments': 1140,
                'rating': 4.7,
            },

            # 비즈니스 & 금융 자격증 (13-20)
            {
                'title': 'SQLD (SQL 개발자) 자격증',
                'slug': 'sqld-sql-developer',
                'category': 'certification',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 99000,
                'short_description': 'SQL 전문가 되기',
                'description': 'SQLD 자격증으로 데이터베이스 전문가의 첫 걸음을 시작합니다.',
                'objectives': ['데이터 모델링', 'SQL 기본', 'SQL 활용', '관리 구문'],
                'duration_hours': 40,
                'enrollments': 3240,
                'rating': 4.7,
            },
            {
                'title': 'SQLP (SQL 전문가) 자격증',
                'slug': 'sqlp-sql-professional',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 159000,
                'short_description': 'SQL 고급 전문가',
                'description': 'SQLP 자격증으로 데이터베이스 고급 전문가가 됩니다.',
                'objectives': ['데이터 모델링 심화', 'SQL 최적화', '튜닝', '아키텍처'],
                'duration_hours': 65,
                'enrollments': 1540,
                'rating': 4.8,
            },
            {
                'title': 'ADsP (데이터분석 준전문가)',
                'slug': 'adsp-data-analysis-associate',
                'category': 'certification',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 119000,
                'short_description': '데이터 분석 입문',
                'description': 'ADsP 자격증으로 데이터 분석 전문가의 길을 시작합니다.',
                'objectives': ['데이터 이해', '데이터 분석 기획', '데이터 분석', '통계 분석'],
                'duration_hours': 45,
                'enrollments': 2840,
                'rating': 4.6,
            },
            {
                'title': 'ADP (데이터분석 전문가)',
                'slug': 'adp-data-analysis-professional',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 179000,
                'short_description': '데이터 분석 전문가',
                'description': 'ADP 자격증으로 데이터 분석 최고 전문가가 됩니다.',
                'objectives': ['데이터 분석 기획', '데이터 분석', '빅데이터', '머신러닝'],
                'duration_hours': 70,
                'enrollments': 1640,
                'rating': 4.8,
            },
            {
                'title': 'CPA (공인회계사) 1차 대비',
                'slug': 'cpa-first-exam',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 299000,
                'short_description': 'CPA 1차 시험 대비',
                'description': 'CPA 1차 시험을 체계적으로 준비합니다.',
                'objectives': ['경영학', '경제학', '상법', '세법개론'],
                'duration_hours': 90,
                'enrollments': 1240,
                'rating': 4.7,
            },
            {
                'title': '세무사 1차 완벽 대비',
                'slug': 'tax-accountant-first-exam',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 279000,
                'short_description': '세무사 1차 합격',
                'description': '세무사 1차 시험을 완벽하게 준비합니다.',
                'objectives': ['재정학', '세법학', '회계학', '상법', '민법'],
                'duration_hours': 85,
                'enrollments': 940,
                'rating': 4.6,
            },
            {
                'title': '공인중개사 자격증',
                'slug': 'real-estate-broker',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 189000,
                'short_description': '공인중개사 한 번에 합격',
                'description': '공인중개사 자격증 시험을 체계적으로 준비합니다.',
                'objectives': ['부동산학개론', '민법', '공인중개사법', '부동산공법', '부동산공시법'],
                'duration_hours': 70,
                'enrollments': 3840,
                'rating': 4.7,
            },
            {
                'title': '관세사 1차 완전 정복',
                'slug': 'customs-broker-first-exam',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 249000,
                'short_description': '관세사 1차 대비',
                'description': '관세사 1차 시험을 완벽하게 준비합니다.',
                'objectives': ['관세법', '무역영어', '내국소비세법', '회계학'],
                'duration_hours': 75,
                'enrollments': 640,
                'rating': 4.8,
            },

            # 전문 자격증 (21-30)
            {
                'title': '변리사 1차 대비',
                'slug': 'patent-attorney-first-exam',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 269000,
                'short_description': '변리사 1차 합격',
                'description': '변리사 1차 시험을 체계적으로 준비합니다.',
                'objectives': ['산업재산권법', '민법', '자연과학개론'],
                'duration_hours': 80,
                'enrollments': 540,
                'rating': 4.7,
            },
            {
                'title': '감정평가사 1차 완벽 대비',
                'slug': 'property-appraiser-first-exam',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 259000,
                'short_description': '감정평가사 1차',
                'description': '감정평가사 1차 시험을 완벽하게 준비합니다.',
                'objectives': ['민법', '경제학원론', '부동산학원론', '감정평가관계법규'],
                'duration_hours': 75,
                'enrollments': 740,
                'rating': 4.6,
            },
            {
                'title': '공인노무사 1차 대비',
                'slug': 'labor-attorney-first-exam',
                'category': 'certification',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 249000,
                'short_description': '공인노무사 1차 합격',
                'description': '공인노무사 1차 시험을 체계적으로 준비합니다.',
                'objectives': ['노동법', '민법', '사회보험법', '경영학', '경제학'],
                'duration_hours': 70,
                'enrollments': 840,
                'rating': 4.7,
            },
            {
                'title': '건축기사 필기 완벽 대비',
                'slug': 'architect-engineer-written',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 149000,
                'short_description': '건축기사 필기 합격',
                'description': '건축기사 필기 시험을 완벽하게 준비합니다.',
                'objectives': ['건축계획', '건축시공', '건축구조', '건축설비', '건축법규'],
                'duration_hours': 55,
                'enrollments': 1840,
                'rating': 4.5,
            },
            {
                'title': '전기기사 필기 완전 정복',
                'slug': 'electrical-engineer-written',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 149000,
                'short_description': '전기기사 필기 대비',
                'description': '전기기사 필기 시험을 체계적으로 준비합니다.',
                'objectives': ['전기자기학', '전력공학', '전기기기', '회로이론', '제어공학'],
                'duration_hours': 55,
                'enrollments': 2140,
                'rating': 4.6,
            },
            {
                'title': '토목기사 필기 대비',
                'slug': 'civil-engineer-written',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 149000,
                'short_description': '토목기사 필기 합격',
                'description': '토목기사 필기 시험을 완벽하게 준비합니다.',
                'objectives': ['응용역학', '토질역학', '수리학', '철근콘크리트', '측량학'],
                'duration_hours': 55,
                'enrollments': 1640,
                'rating': 4.5,
            },
            {
                'title': '산업안전기사 필기 완벽 대비',
                'slug': 'industrial-safety-engineer-written',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 139000,
                'short_description': '산업안전기사 필기',
                'description': '산업안전기사 필기 시험을 체계적으로 준비합니다.',
                'objectives': ['안전관리론', '인간공학', '기계위험방지기술', '전기위험방지기술', '화학설비위험방지기술'],
                'duration_hours': 50,
                'enrollments': 2340,
                'rating': 4.6,
            },
            {
                'title': '위험물산업기사 완전 정복',
                'slug': 'hazardous-materials-engineer',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 129000,
                'short_description': '위험물산업기사 대비',
                'description': '위험물산업기사 시험을 완벽하게 준비합니다.',
                'objectives': ['일반화학', '화재예방과 소화방법', '위험물의 성질', '위험물 관련 법규'],
                'duration_hours': 45,
                'enrollments': 1740,
                'rating': 4.5,
            },
            {
                'title': '소방설비기사(전기) 필기 대비',
                'slug': 'fire-protection-engineer-electrical',
                'category': 'certification',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 149000,
                'short_description': '소방설비기사(전기) 필기',
                'description': '소방설비기사(전기) 필기 시험을 체계적으로 준비합니다.',
                'objectives': ['소방원론', '소방전기일반', '소방관계법규', '소방전기시설의 구조 및 원리'],
                'duration_hours': 50,
                'enrollments': 1540,
                'rating': 4.6,
            },
            {
                'title': '컴퓨터활용능력 1급',
                'slug': 'computer-proficiency-level1',
                'category': 'certification',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '컴활 1급 한 번에 합격',
                'description': '컴퓨터활용능력 1급 시험을 완벽하게 준비합니다.',
                'objectives': ['컴퓨터 일반', '스프레드시트 일반', '스프레드시트 실무', '데이터베이스 일반', '데이터베이스 실무'],
                'duration_hours': 35,
                'enrollments': 5840,
                'rating': 4.7,
            },
        ]

        created_count = 0
        for course_data in courses_data:
            if Course.objects.filter(slug=course_data['slug']).exists():
                self.stdout.write(f'  ⏭️  Skipping {course_data["slug"]}')
                continue

            # Get random instructor
            instructor = random.choice(instructors)

            # Extract fields
            objectives = course_data.pop('objectives')
            price = course_data.pop('price', 0)
            duration = course_data.pop('duration_hours', 40)
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
            module_titles = ['시험 소개', '이론 학습', '문제 풀이', '실전 모의고사', '최종 정리']
            for idx, title in enumerate(module_titles[:4]):
                module = Module.objects.create(
                    course=course,
                    title=title,
                    description=f'{title} 단계 학습',
                    order=idx
                )
                for les_idx in range(3):
                    Lesson.objects.create(
                        module=module,
                        title=f'{title} {les_idx + 1}',
                        lesson_type='video',
                        content=f'{title}의 학습 내용입니다.',
                        order=les_idx,
                        is_preview=(idx == 0 and les_idx == 0),
                        video_duration=random.randint(600, 2400)
                    )

            # Create practice questions
            for _ in range(10):
                PracticeQuestion.objects.create(
                    course=course,
                    topic=course.title.split()[0],
                    difficulty=random.choice(['easy', 'medium', 'hard']),
                    question=f'{course.title}에 대한 연습 문제입니다.',
                    options=['선택지 1', '선택지 2', '선택지 3', '선택지 4'],
                    correct_answer='선택지 1',
                    explanation='정답에 대한 설명입니다.'
                )

            created_count += 1
            self.stdout.write(f'  ✅ [{created_count}/30] {course.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully created {created_count} certification courses!'
                f'\n📚 Categories:'
                f'\n   - IT 자격증 (12개): 정보처리기사, AWS, GCP, CompTIA, CCNA, CISSP, PMP, CKA, CKAD, RHCSA, SQLD, SQLP'
                f'\n   - 비즈니스 & 금융 (8개): ADsP, ADP, CPA, 세무사, 공인중개사, 관세사'
                f'\n   - 전문 자격증 (10개): 변리사, 감정평가사, 노무사, 건축/전기/토목기사, 산업안전기사, 위험물, 소방설비기사, 컴활'
            )
        )
