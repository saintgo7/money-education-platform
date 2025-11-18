from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
from django.utils.text import slugify
import random

User = get_user_model()


class Command(BaseCommand):
    help = '50개의 학습 프로그램(코스)을 생성합니다'

    def handle(self, *args, **options):
        self.stdout.write('코스 데이터 생성 시작...')

        # 강사 계정 생성 또는 가져오기
        instructors = []
        instructor_names = [
            ('김민수', 'minsu'),
            ('이지은', 'jieun'),
            ('박준호', 'junho'),
            ('최서연', 'seoyeon'),
            ('정대현', 'daehyun'),
            ('강하늘', 'haneul'),
            ('송지아', 'jia'),
            ('윤성호', 'seongho'),
        ]

        for name, username in instructor_names:
            instructor, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': name.split()[0],
                    'last_name': name.split()[1] if len(name.split()) > 1 else '',
                    'user_type': 'instructor',
                }
            )
            if created:
                instructor.set_password('password123')
                instructor.save()
            instructors.append(instructor)

        # 코스 데이터
        courses_data = [
            # 금융 카테고리 (10개)
            {
                'title': '초보자를 위한 주식 투자 입문',
                'category': 'finance',
                'difficulty': 'beginner',
                'short_description': '주식 시장의 기초부터 첫 투자까지',
                'description': '주식 투자의 기본 개념과 원리를 배우고, 안전하게 첫 투자를 시작하는 방법을 알려드립니다.',
                'price': 49000,
                'price_type': 'paid',
            },
            {
                'title': '부동산 투자 완벽 가이드',
                'category': 'finance',
                'difficulty': 'intermediate',
                'short_description': '부동산 시장 분석부터 투자 전략까지',
                'description': '부동산 투자의 A to Z를 배우고, 실전 투자 전략을 수립하는 방법을 학습합니다.',
                'price': 89000,
                'price_type': 'paid',
            },
            {
                'title': '암호화폐와 블록체인 투자',
                'category': 'finance',
                'difficulty': 'intermediate',
                'short_description': '비트코인부터 DeFi까지 완벽 이해',
                'description': '암호화폐 시장의 동향을 분석하고, 안전한 투자 방법을 배웁니다.',
                'price': 69000,
                'price_type': 'paid',
            },
            {
                'title': '재무제표 읽는 법',
                'category': 'finance',
                'difficulty': 'beginner',
                'short_description': '숫자로 기업 가치 파악하기',
                'description': '재무제표의 기본 구조를 이해하고, 기업의 재무 상태를 분석하는 방법을 배웁니다.',
                'price': 39000,
                'price_type': 'paid',
            },
            {
                'title': '퀀트 투자 전략 마스터',
                'category': 'finance',
                'difficulty': 'advanced',
                'short_description': '데이터 기반 투자 전략 수립',
                'description': '통계와 데이터 분석을 활용한 체계적인 투자 전략을 학습합니다.',
                'price': 129000,
                'price_type': 'paid',
            },
            {
                'title': '개인 재무관리와 자산 배분',
                'category': 'finance',
                'difficulty': 'beginner',
                'short_description': '돈 모으는 습관부터 포트폴리오까지',
                'description': '효과적인 개인 재무 관리 방법과 자산 배분 전략을 배웁니다.',
                'price': 29000,
                'price_type': 'paid',
            },
            {
                'title': 'ETF 투자 완벽 가이드',
                'category': 'finance',
                'difficulty': 'beginner',
                'short_description': '분산 투자로 안정적 수익 창출',
                'description': 'ETF의 기본 개념부터 포트폴리오 구성까지 완벽하게 학습합니다.',
                'price': 49000,
                'price_type': 'paid',
            },
            {
                'title': '채권 투자와 금리 분석',
                'category': 'finance',
                'difficulty': 'intermediate',
                'short_description': '안정적 수익을 위한 채권 투자',
                'description': '채권의 종류와 특징을 이해하고, 금리 변동에 따른 투자 전략을 배웁니다.',
                'price': 59000,
                'price_type': 'paid',
            },
            {
                'title': '파생상품과 헤지 전략',
                'category': 'finance',
                'difficulty': 'advanced',
                'short_description': '옵션, 선물로 위험 관리하기',
                'description': '파생상품의 원리를 이해하고, 포트폴리오 헤지 전략을 수립합니다.',
                'price': 149000,
                'price_type': 'paid',
            },
            {
                'title': '세금 절세 전략',
                'category': 'finance',
                'difficulty': 'intermediate',
                'short_description': '합법적으로 세금 줄이는 방법',
                'description': '투자 수익에 대한 세금을 최소화하는 다양한 절세 전략을 배웁니다.',
                'price': 79000,
                'price_type': 'paid',
            },

            # 프로그래밍 카테고리 (10개)
            {
                'title': 'Python 기초부터 실전까지',
                'category': 'programming',
                'difficulty': 'beginner',
                'short_description': '프로그래밍 입문자를 위한 파이썬',
                'description': 'Python의 기본 문법부터 실전 프로젝트까지 단계별로 학습합니다.',
                'price': 59000,
                'price_type': 'paid',
            },
            {
                'title': 'JavaScript 완벽 마스터',
                'category': 'programming',
                'difficulty': 'intermediate',
                'short_description': '모던 JavaScript ES6+',
                'description': '최신 JavaScript 문법과 비동기 프로그래밍을 마스터합니다.',
                'price': 69000,
                'price_type': 'paid',
            },
            {
                'title': 'React로 만드는 현대적 웹앱',
                'category': 'programming',
                'difficulty': 'intermediate',
                'short_description': 'React Hooks와 Context API',
                'description': 'React를 사용한 SPA 개발과 상태 관리를 배웁니다.',
                'price': 89000,
                'price_type': 'paid',
            },
            {
                'title': 'Node.js 백엔드 개발',
                'category': 'programming',
                'difficulty': 'intermediate',
                'short_description': 'Express와 MongoDB로 API 구축',
                'description': 'Node.js로 RESTful API를 개발하고 데이터베이스를 연동합니다.',
                'price': 99000,
                'price_type': 'paid',
            },
            {
                'title': 'Django로 만드는 풀스택 웹서비스',
                'category': 'programming',
                'difficulty': 'advanced',
                'short_description': 'Python 웹 프레임워크 마스터',
                'description': 'Django를 활용한 완전한 웹 서비스 개발을 학습합니다.',
                'price': 129000,
                'price_type': 'paid',
            },
            {
                'title': 'SQL 데이터베이스 완벽 가이드',
                'category': 'programming',
                'difficulty': 'beginner',
                'short_description': '데이터베이스 설계부터 쿼리까지',
                'description': 'SQL의 기초부터 고급 쿼리 작성까지 완벽하게 배웁니다.',
                'price': 49000,
                'price_type': 'paid',
            },
            {
                'title': 'Git과 GitHub 협업 실무',
                'category': 'programming',
                'difficulty': 'beginner',
                'short_description': '버전 관리와 팀 협업',
                'description': 'Git의 기본 개념부터 GitHub를 활용한 협업 전략까지 배웁니다.',
                'price': 29000,
                'price_type': 'paid',
            },
            {
                'title': 'Docker와 Kubernetes 입문',
                'category': 'programming',
                'difficulty': 'advanced',
                'short_description': '컨테이너 기반 배포 자동화',
                'description': 'Docker와 Kubernetes를 활용한 컨테이너 오케스트레이션을 배웁니다.',
                'price': 149000,
                'price_type': 'paid',
            },
            {
                'title': 'AWS 클라우드 아키텍처',
                'category': 'programming',
                'difficulty': 'advanced',
                'short_description': '클라우드 인프라 설계와 구축',
                'description': 'AWS 서비스를 활용한 확장 가능한 클라우드 아키텍처를 설계합니다.',
                'price': 179000,
                'price_type': 'paid',
            },
            {
                'title': '알고리즘과 자료구조',
                'category': 'programming',
                'difficulty': 'intermediate',
                'short_description': '코딩 테스트 완벽 대비',
                'description': '핵심 알고리즘과 자료구조를 배우고 문제 해결 능력을 키웁니다.',
                'price': 79000,
                'price_type': 'paid',
            },

            # 데이터 사이언스 카테고리 (10개)
            {
                'title': '데이터 분석 입문 with Python',
                'category': 'data_science',
                'difficulty': 'beginner',
                'short_description': 'Pandas와 NumPy로 시작하기',
                'description': 'Python을 활용한 데이터 분석의 기초를 배우고 실전 프로젝트를 진행합니다.',
                'price': 69000,
                'price_type': 'paid',
            },
            {
                'title': '머신러닝 완벽 가이드',
                'category': 'data_science',
                'difficulty': 'intermediate',
                'short_description': 'Scikit-learn으로 배우는 ML',
                'description': '지도학습, 비지도학습 알고리즘을 이해하고 실전 적용 방법을 배웁니다.',
                'price': 119000,
                'price_type': 'paid',
            },
            {
                'title': '딥러닝과 인공신경망',
                'category': 'data_science',
                'difficulty': 'advanced',
                'short_description': 'TensorFlow와 PyTorch',
                'description': 'CNN, RNN 등 다양한 신경망 구조를 학습하고 실전 프로젝트를 진행합니다.',
                'price': 159000,
                'price_type': 'paid',
            },
            {
                'title': '데이터 시각화 마스터',
                'category': 'data_science',
                'difficulty': 'beginner',
                'short_description': 'Matplotlib, Seaborn, Plotly',
                'description': '효과적인 데이터 시각화 기법을 배우고 인사이트를 도출합니다.',
                'price': 49000,
                'price_type': 'paid',
            },
            {
                'title': 'SQL for Data Analysis',
                'category': 'data_science',
                'difficulty': 'intermediate',
                'short_description': '데이터 분석을 위한 고급 SQL',
                'description': '복잡한 데이터 분석을 위한 고급 SQL 쿼리와 윈도우 함수를 마스터합니다.',
                'price': 59000,
                'price_type': 'paid',
            },
            {
                'title': '자연어 처리 NLP 실전',
                'category': 'data_science',
                'difficulty': 'advanced',
                'short_description': 'BERT, GPT 활용하기',
                'description': '최신 NLP 기술을 배우고 텍스트 분석 프로젝트를 진행합니다.',
                'price': 169000,
                'price_type': 'paid',
            },
            {
                'title': '통계학으로 배우는 데이터 분석',
                'category': 'data_science',
                'difficulty': 'intermediate',
                'short_description': '확률과 통계의 실전 적용',
                'description': '데이터 분석에 필요한 통계학 기초와 가설 검정을 배웁니다.',
                'price': 79000,
                'price_type': 'paid',
            },
            {
                'title': 'A/B 테스트와 실험 설계',
                'category': 'data_science',
                'difficulty': 'intermediate',
                'short_description': '데이터 기반 의사결정',
                'description': 'A/B 테스트 설계부터 결과 분석까지 실전 경험을 쌓습니다.',
                'price': 89000,
                'price_type': 'paid',
            },
            {
                'title': '추천 시스템 구축하기',
                'category': 'data_science',
                'difficulty': 'advanced',
                'short_description': '협업 필터링과 딥러닝',
                'description': '다양한 추천 알고리즘을 배우고 실제 추천 시스템을 구축합니다.',
                'price': 149000,
                'price_type': 'paid',
            },
            {
                'title': '시계열 데이터 분석',
                'category': 'data_science',
                'difficulty': 'intermediate',
                'short_description': 'ARIMA, Prophet으로 예측하기',
                'description': '시계열 데이터의 특성을 이해하고 미래 값을 예측하는 모델을 만듭니다.',
                'price': 99000,
                'price_type': 'paid',
            },

            # 비즈니스 카테고리 (10개)
            {
                'title': '스타트업 창업 완벽 가이드',
                'category': 'business',
                'difficulty': 'beginner',
                'short_description': '아이디어부터 투자 유치까지',
                'description': '스타트업 창업의 모든 과정을 배우고 성공적인 비즈니스를 시작합니다.',
                'price': 99000,
                'price_type': 'paid',
            },
            {
                'title': '린 스타트업 방법론',
                'category': 'business',
                'difficulty': 'intermediate',
                'short_description': '빠르게 검증하고 성장하기',
                'description': 'MVP 개발, 피봇, 린 캔버스 등 린 스타트업 핵심 개념을 학습합니다.',
                'price': 79000,
                'price_type': 'paid',
            },
            {
                'title': '프로젝트 관리 실무',
                'category': 'business',
                'difficulty': 'intermediate',
                'short_description': 'Agile과 Scrum 마스터',
                'description': '애자일 방법론을 적용한 효과적인 프로젝트 관리 기법을 배웁니다.',
                'price': 89000,
                'price_type': 'paid',
            },
            {
                'title': '비즈니스 모델 캔버스',
                'category': 'business',
                'difficulty': 'beginner',
                'short_description': '성공하는 비즈니스 모델 설계',
                'description': '비즈니스 모델 캔버스를 활용한 체계적인 사업 계획을 수립합니다.',
                'price': 59000,
                'price_type': 'paid',
            },
            {
                'title': '데이터 기반 의사결정',
                'category': 'business',
                'difficulty': 'intermediate',
                'short_description': 'KPI 설정과 성과 측정',
                'description': '데이터를 활용한 의사결정 프로세스와 KPI 관리 방법을 배웁니다.',
                'price': 79000,
                'price_type': 'paid',
            },
            {
                'title': '협상의 기술',
                'category': 'business',
                'difficulty': 'intermediate',
                'short_description': 'Win-Win 협상 전략',
                'description': '비즈니스 협상의 원칙과 실전 테크닉을 배우고 연습합니다.',
                'price': 69000,
                'price_type': 'paid',
            },
            {
                'title': '비즈니스 영어 커뮤니케이션',
                'category': 'business',
                'difficulty': 'intermediate',
                'short_description': '글로벌 비즈니스를 위한 영어',
                'description': '이메일, 프레젠테이션, 회의 등 실무 영어 커뮤니케이션을 마스터합니다.',
                'price': 89000,
                'price_type': 'paid',
            },
            {
                'title': '프레젠테이션 스킬',
                'category': 'business',
                'difficulty': 'beginner',
                'short_description': '설득력 있는 발표 만들기',
                'description': '청중을 사로잡는 프레젠테이션 기획, 디자인, 발표 기법을 배웁니다.',
                'price': 49000,
                'price_type': 'paid',
            },
            {
                'title': 'B2B 세일즈 전략',
                'category': 'business',
                'difficulty': 'advanced',
                'short_description': '기업 고객 영업 마스터',
                'description': 'B2B 세일즈 프로세스와 대형 거래 성사 전략을 배웁니다.',
                'price': 129000,
                'price_type': 'paid',
            },
            {
                'title': '공급망 관리 SCM',
                'category': 'business',
                'difficulty': 'advanced',
                'short_description': '효율적인 물류와 재고 관리',
                'description': '공급망 최적화와 재고 관리 전략을 학습합니다.',
                'price': 119000,
                'price_type': 'paid',
            },

            # 마케팅 카테고리 (10개)
            {
                'title': '디지털 마케팅 완벽 가이드',
                'category': 'marketing',
                'difficulty': 'beginner',
                'short_description': 'SEO, SNS, 콘텐츠 마케팅',
                'description': '디지털 시대의 핵심 마케팅 채널과 전략을 모두 배웁니다.',
                'price': 79000,
                'price_type': 'paid',
            },
            {
                'title': '퍼포먼스 마케팅 실전',
                'category': 'marketing',
                'difficulty': 'intermediate',
                'short_description': 'Google Ads, Facebook Ads',
                'description': 'ROI 중심의 퍼포먼스 마케팅 캠페인 운영 방법을 배웁니다.',
                'price': 99000,
                'price_type': 'paid',
            },
            {
                'title': 'SEO 최적화 전략',
                'category': 'marketing',
                'difficulty': 'intermediate',
                'short_description': '검색 엔진 상위 노출의 비밀',
                'description': '기술적 SEO부터 콘텐츠 최적화까지 체계적으로 학습합니다.',
                'price': 69000,
                'price_type': 'paid',
            },
            {
                'title': '콘텐츠 마케팅 전략',
                'category': 'marketing',
                'difficulty': 'beginner',
                'short_description': '가치 있는 콘텐츠로 고객 유치',
                'description': '콘텐츠 기획부터 배포, 성과 측정까지 전 과정을 배웁니다.',
                'price': 59000,
                'price_type': 'paid',
            },
            {
                'title': 'SNS 마케팅 마스터',
                'category': 'marketing',
                'difficulty': 'beginner',
                'short_description': '인스타그램, 유튜브 활용법',
                'description': '각 SNS 플랫폼의 특성을 이해하고 효과적인 마케팅 전략을 수립합니다.',
                'price': 49000,
                'price_type': 'paid',
            },
            {
                'title': '브랜딩의 모든 것',
                'category': 'marketing',
                'difficulty': 'intermediate',
                'short_description': '강력한 브랜드 만들기',
                'description': '브랜드 아이덴티티 구축부터 브랜드 경험 설계까지 배웁니다.',
                'price': 89000,
                'price_type': 'paid',
            },
            {
                'title': '이메일 마케팅 실전',
                'category': 'marketing',
                'difficulty': 'beginner',
                'short_description': '높은 전환율의 이메일 캠페인',
                'description': '효과적인 이메일 마케팅 전략과 자동화 도구 활용법을 배웁니다.',
                'price': 39000,
                'price_type': 'paid',
            },
            {
                'title': 'Growth Hacking',
                'category': 'marketing',
                'difficulty': 'advanced',
                'short_description': '빠른 성장을 위한 실험과 최적화',
                'description': '데이터 기반 성장 전략과 실험 방법론을 마스터합니다.',
                'price': 129000,
                'price_type': 'paid',
            },
            {
                'title': '구글 애널리틱스 GA4',
                'category': 'marketing',
                'difficulty': 'intermediate',
                'short_description': '데이터로 마케팅 성과 측정',
                'description': 'GA4를 활용한 웹사이트 분석과 마케팅 ROI 측정을 배웁니다.',
                'price': 69000,
                'price_type': 'paid',
            },
            {
                'title': '바이럴 마케팅 전략',
                'category': 'marketing',
                'difficulty': 'intermediate',
                'short_description': '입소문 나는 콘텐츠 만들기',
                'description': '바이럴 마케팅의 원리와 실전 캠페인 기획 방법을 배웁니다.',
                'price': 79000,
                'price_type': 'paid',
            },
        ]

        # 코스 생성
        created_count = 0
        for course_data in courses_data:
            instructor = random.choice(instructors)

            # 할인가 랜덤 생성 (30%는 할인 적용)
            discount_price = None
            if random.random() < 0.3:
                discount_price = int(course_data['price'] * 0.7)  # 30% 할인

            course = Course.objects.create(
                title=course_data['title'],
                slug=slugify(course_data['title'], allow_unicode=True),
                short_description=course_data['short_description'],
                description=course_data['description'],
                instructor=instructor,
                category=course_data['category'],
                difficulty=course_data['difficulty'],
                price=course_data['price'],
                discount_price=discount_price,
                price_type=course_data['price_type'],
                is_published=True,
                total_duration_minutes=random.randint(180, 1200),  # 3~20시간
            )

            # 각 코스에 모듈과 레슨 생성
            num_modules = random.randint(3, 6)
            for module_num in range(1, num_modules + 1):
                module = Module.objects.create(
                    course=course,
                    title=f'모듈 {module_num}: {self.get_module_title(course_data["category"])}',
                    description=f'{course_data["title"]}의 {module_num}번째 모듈입니다.',
                    order=module_num,
                )

                # 각 모듈에 레슨 생성
                num_lessons = random.randint(4, 8)
                lesson_types = ['video', 'text', 'quiz', 'assignment']

                for lesson_num in range(1, num_lessons + 1):
                    lesson_type = random.choice(lesson_types)
                    is_preview = lesson_num == 1  # 첫 번째 레슨은 미리보기 가능

                    Lesson.objects.create(
                        module=module,
                        title=f'레슨 {lesson_num}: {self.get_lesson_title(lesson_type)}',
                        lesson_type=lesson_type,
                        order=lesson_num,
                        content=f'이것은 {course_data["title"]}의 레슨 내용입니다.' if lesson_type == 'text' else None,
                        video_url=f'https://example.com/videos/{course.slug}-{module_num}-{lesson_num}.mp4' if lesson_type == 'video' else None,
                        video_duration=random.randint(300, 1800) if lesson_type == 'video' else 0,
                        is_preview=is_preview,
                    )

            created_count += 1
            self.stdout.write(f'✓ {course.title} 생성 완료 ({created_count}/50)')

        self.stdout.write(self.style.SUCCESS(f'\n성공적으로 {created_count}개의 코스를 생성했습니다!'))

    def get_module_title(self, category):
        """카테고리별 모듈 제목 생성"""
        titles = {
            'finance': ['기초 이론', '실전 전략', '사례 연구', '위험 관리', '고급 테크닉'],
            'programming': ['기본 문법', '핵심 개념', '실전 프로젝트', '최적화', '배포'],
            'data_science': ['데이터 전처리', '탐색적 분석', '모델 개발', '성능 평가', '실전 응용'],
            'business': ['기초 개념', '실전 전략', '사례 연구', '협업 도구', '심화 학습'],
            'marketing': ['마케팅 기초', '채널 전략', '캠페인 기획', '성과 분석', '고급 기법'],
        }
        return random.choice(titles.get(category, ['기본', '중급', '고급', '심화', '실전']))

    def get_lesson_title(self, lesson_type):
        """레슨 타입별 제목 생성"""
        titles = {
            'video': ['핵심 개념 강의', '실습 따라하기', '사례 분석', '전문가 인터뷰'],
            'text': ['이론 학습', '개념 정리', '가이드라인', '체크리스트'],
            'quiz': ['이해도 체크', '실력 테스트', '종합 퀴즈', '복습 문제'],
            'assignment': ['실전 과제', '프로젝트 실습', '케이스 스터디', '포트폴리오 만들기'],
        }
        return random.choice(titles.get(lesson_type, ['학습 자료']))
