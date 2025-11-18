"""
Management command to create 50 diverse sample courses
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
from ai.models import PracticeQuestion
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create 50 diverse sample courses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating 50 sample courses...')

        # Get or create instructor
        try:
            instructor = User.objects.get(username='instructor1')
        except User.DoesNotExist:
            instructor = User.objects.create_user(
                username='instructor1',
                email='instructor@example.com',
                password='instructor123',
                first_name='John',
                last_name='Doe',
                user_type='instructor',
                verified_instructor=True
            )

        # Create additional instructors for variety
        instructors = [instructor]
        instructor_names = [
            ('김민수', 'Kim', 'Minsu'),
            ('이지은', 'Lee', 'Jieun'),
            ('박준호', 'Park', 'Junho'),
            ('최서연', 'Choi', 'Seoyeon'),
            ('정태희', 'Jung', 'Taehee'),
        ]

        for idx, (full_name, last, first) in enumerate(instructor_names, 2):
            username = f'instructor{idx}'
            if not User.objects.filter(username=username).exists():
                new_instructor = User.objects.create_user(
                    username=username,
                    email=f'instructor{idx}@example.com',
                    password='instructor123',
                    first_name=first,
                    last_name=last,
                    user_type='instructor',
                    verified_instructor=True
                )
                instructors.append(new_instructor)
            else:
                instructors.append(User.objects.get(username=username))

        # 50 diverse courses
        courses_data = [
            # 프로그래밍 (1-15)
            {
                'title': 'Python 완벽 가이드 - 기초부터 실전까지',
                'slug': 'python-complete-guide',
                'category': 'programming',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '파이썬 기초부터 실전 프로젝트까지 한 번에',
                'description': '''파이썬의 모든 것을 배우는 완벽한 코스입니다.

✓ 변수, 함수, 클래스 등 기본 문법
✓ 데이터 구조와 알고리즘
✓ 파일 처리와 예외 처리
✓ 실전 프로젝트 3개''',
                'objectives': ['Python 기본 문법 완벽 이해', '객체지향 프로그래밍', '실전 프로젝트 개발', '디버깅 능력 향상']
            },
            {
                'title': 'JavaScript 마스터클래스',
                'slug': 'javascript-masterclass',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 59000,
                'short_description': 'ES6+부터 비동기까지 완벽 마스터',
                'description': 'JavaScript를 깊이 있게 배우고 현대적인 웹 개발자가 되세요.',
                'objectives': ['ES6+ 문법 마스터', '비동기 프로그래밍', 'DOM 조작', '모던 JavaScript 패턴']
            },
            {
                'title': 'React 완벽 가이드',
                'slug': 'react-complete-guide',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 79000,
                'short_description': 'React Hooks부터 Next.js까지',
                'description': 'React의 기초부터 고급 패턴까지 모두 배웁니다.',
                'objectives': ['React Hooks 마스터', '상태 관리', 'Next.js 활용', '성능 최적화']
            },
            {
                'title': 'Node.js 백엔드 개발',
                'slug': 'nodejs-backend-development',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 69000,
                'short_description': 'Express로 RESTful API 만들기',
                'description': 'Node.js로 확장 가능한 백엔드를 개발합니다.',
                'objectives': ['Express.js 마스터', 'REST API 설계', 'MongoDB 연동', '인증/보안']
            },
            {
                'title': 'Django 풀스택 웹 개발',
                'slug': 'django-fullstack',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 89000,
                'short_description': 'Django로 완벽한 웹 서비스 만들기',
                'description': 'Django 프레임워크로 실전 웹 서비스를 개발합니다.',
                'objectives': ['Django 프레임워크', 'ORM과 데이터베이스', 'REST API', '배포 및 운영']
            },
            {
                'title': 'Java 프로그래밍 입문',
                'slug': 'java-programming-basics',
                'category': 'programming',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '자바 기초부터 차근차근',
                'description': 'Java의 기본을 탄탄하게 다집니다.',
                'objectives': ['Java 기본 문법', '객체지향 개념', '컬렉션 프레임워크', '예외 처리']
            },
            {
                'title': 'Spring Boot 마스터',
                'slug': 'spring-boot-master',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 99000,
                'short_description': 'Spring Boot로 엔터프라이즈 앱 개발',
                'description': 'Spring Boot를 활용한 실무 백엔드 개발을 배웁니다.',
                'objectives': ['Spring Boot 핵심', 'JPA와 Hibernate', 'Security 구현', '마이크로서비스']
            },
            {
                'title': 'C++ 게임 프로그래밍',
                'slug': 'cpp-game-programming',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 129000,
                'short_description': 'Unreal Engine과 C++로 게임 만들기',
                'description': 'C++와 언리얼 엔진으로 3D 게임을 제작합니다.',
                'objectives': ['C++ 고급 문법', 'Unreal Engine 기초', '게임 로직 구현', '3D 그래픽스']
            },
            {
                'title': 'Go 언어 백엔드 개발',
                'slug': 'golang-backend',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 75000,
                'short_description': 'Go로 고성능 서버 만들기',
                'description': 'Go 언어로 빠르고 안정적인 백엔드를 개발합니다.',
                'objectives': ['Go 언어 기초', 'Goroutine과 Channel', 'RESTful API', '마이크로서비스']
            },
            {
                'title': 'TypeScript 완벽 가이드',
                'slug': 'typescript-complete',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 65000,
                'short_description': 'TypeScript로 안전한 코드 작성하기',
                'description': 'TypeScript의 타입 시스템을 완벽하게 이해합니다.',
                'objectives': ['TypeScript 기초', '고급 타입', '제네릭', '실전 프로젝트']
            },
            {
                'title': 'Flutter 모바일 앱 개발',
                'slug': 'flutter-mobile-dev',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 89000,
                'short_description': 'Flutter로 크로스플랫폼 앱 만들기',
                'description': 'Flutter로 iOS/Android 앱을 동시에 개발합니다.',
                'objectives': ['Flutter 기초', 'Widget 마스터', '상태 관리', '앱 배포']
            },
            {
                'title': 'Rust 시스템 프로그래밍',
                'slug': 'rust-system-programming',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 95000,
                'short_description': 'Rust로 안전하고 빠른 프로그램 개발',
                'description': 'Rust의 소유권 시스템과 메모리 안전성을 배웁니다.',
                'objectives': ['Rust 기본 문법', '소유권과 차용', '동시성 프로그래밍', '시스템 개발']
            },
            {
                'title': 'Swift iOS 앱 개발',
                'slug': 'swift-ios-development',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 99000,
                'short_description': 'Swift와 SwiftUI로 iOS 앱 만들기',
                'description': 'Swift 언어로 네이티브 iOS 앱을 개발합니다.',
                'objectives': ['Swift 문법', 'SwiftUI', 'Core Data', 'App Store 배포']
            },
            {
                'title': 'Kotlin Android 개발',
                'slug': 'kotlin-android',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 95000,
                'short_description': 'Kotlin으로 안드로이드 앱 개발',
                'description': 'Kotlin과 Jetpack Compose로 모던 Android 앱을 만듭니다.',
                'objectives': ['Kotlin 기초', 'Jetpack Compose', 'Room Database', 'Google Play 배포']
            },
            {
                'title': 'PHP Laravel 웹 개발',
                'slug': 'php-laravel',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 69000,
                'short_description': 'Laravel로 현대적인 웹 앱 개발',
                'description': 'Laravel 프레임워크로 웹 애플리케이션을 개발합니다.',
                'objectives': ['Laravel 기초', 'Eloquent ORM', 'Blade 템플릿', 'API 개발']
            },

            # 데이터 사이언스 & AI (16-25)
            {
                'title': '머신러닝 기초부터 실전까지',
                'slug': 'machine-learning-complete',
                'category': 'data-science',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 99000,
                'short_description': 'Python으로 배우는 머신러닝',
                'description': '머신러닝의 기초 이론부터 실전 프로젝트까지 완벽하게 학습합니다.',
                'objectives': ['ML 기본 개념', 'Scikit-learn', '실전 프로젝트', '모델 배포']
            },
            {
                'title': '딥러닝과 신경망',
                'slug': 'deep-learning-neural-networks',
                'category': 'data-science',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 129000,
                'short_description': 'TensorFlow와 PyTorch로 배우는 딥러닝',
                'description': '딥러닝의 핵심 개념과 최신 기술을 마스터합니다.',
                'objectives': ['신경망 기초', 'CNN/RNN', 'Transformer', '실전 프로젝트']
            },
            {
                'title': '데이터 분석 with Python',
                'slug': 'data-analysis-python',
                'category': 'data-science',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 79000,
                'short_description': 'Pandas와 NumPy로 데이터 분석',
                'description': 'Python을 활용한 데이터 분석의 모든 것을 배웁니다.',
                'objectives': ['Pandas 마스터', '데이터 시각화', '통계 분석', '실전 분석']
            },
            {
                'title': 'SQL 데이터베이스 완벽 가이드',
                'slug': 'sql-database-guide',
                'category': 'data-science',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': 'SQL 기초부터 고급 쿼리까지',
                'description': 'SQL의 모든 것을 배우고 데이터베이스를 마스터합니다.',
                'objectives': ['SQL 기본 문법', '조인과 서브쿼리', '인덱스 최적화', '실전 쿼리']
            },
            {
                'title': 'ChatGPT API 활용 개발',
                'slug': 'chatgpt-api-development',
                'category': 'data-science',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 89000,
                'short_description': 'GPT API로 AI 앱 만들기',
                'description': 'OpenAI API를 활용하여 실용적인 AI 서비스를 개발합니다.',
                'objectives': ['OpenAI API', 'Prompt Engineering', 'AI 앱 개발', '배포 전략']
            },
            {
                'title': 'LangChain으로 만드는 AI 에이전트',
                'slug': 'langchain-ai-agents',
                'category': 'data-science',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 119000,
                'short_description': 'LLM 기반 자동화 시스템 구축',
                'description': 'LangChain을 활용하여 지능형 AI 에이전트를 만듭니다.',
                'objectives': ['LangChain 기초', 'Agent 설계', 'RAG 구현', '실전 프로젝트']
            },
            {
                'title': '컴퓨터 비전 with OpenCV',
                'slug': 'computer-vision-opencv',
                'category': 'data-science',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '이미지 처리와 객체 인식',
                'description': 'OpenCV로 컴퓨터 비전의 기초부터 응용까지 배웁니다.',
                'objectives': ['OpenCV 기초', '이미지 처리', '객체 감지', '실시간 비전']
            },
            {
                'title': '자연어 처리 NLP 완벽 가이드',
                'slug': 'nlp-complete-guide',
                'category': 'data-science',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 119000,
                'short_description': 'Transformer부터 BERT까지',
                'description': '최신 NLP 기술을 마스터하고 실전 프로젝트를 진행합니다.',
                'objectives': ['NLP 기초', 'Transformer', 'BERT/GPT', '실전 응용']
            },
            {
                'title': 'Tableau 데이터 시각화',
                'slug': 'tableau-data-visualization',
                'category': 'data-science',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 69000,
                'short_description': 'Tableau로 인사이트 발견하기',
                'description': 'Tableau를 활용하여 효과적인 데이터 시각화를 만듭니다.',
                'objectives': ['Tableau 기초', '대시보드 제작', '고급 시각화', '스토리텔링']
            },
            {
                'title': 'Apache Spark 빅데이터 처리',
                'slug': 'apache-spark-bigdata',
                'category': 'data-science',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 139000,
                'short_description': 'Spark로 대용량 데이터 처리',
                'description': 'Apache Spark를 활용한 빅데이터 처리와 분석을 마스터합니다.',
                'objectives': ['Spark 기초', 'PySpark', '분산 처리', '실시간 분석']
            },

            # 디자인 (26-32)
            {
                'title': 'UI/UX 디자인 완벽 가이드',
                'slug': 'uiux-design-complete',
                'category': 'design',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '사용자 중심 디자인 마스터',
                'description': 'UI/UX의 기초부터 실전 프로젝트까지 완벽하게 학습합니다.',
                'objectives': ['디자인 원칙', '사용자 리서치', 'Figma 마스터', '프로토타이핑']
            },
            {
                'title': 'Figma 완벽 마스터',
                'slug': 'figma-master',
                'category': 'design',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': 'Figma로 프로페셔널 디자인',
                'description': 'Figma의 모든 기능을 마스터하고 실전 디자인을 제작합니다.',
                'objectives': ['Figma 기초', '컴포넌트 시스템', '프로토타입', '협업 워크플로우']
            },
            {
                'title': 'Adobe XD 웹/앱 디자인',
                'slug': 'adobe-xd-design',
                'category': 'design',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 75000,
                'short_description': 'XD로 인터랙티브 디자인',
                'description': 'Adobe XD를 활용한 웹과 모바일 앱 디자인을 배웁니다.',
                'objectives': ['XD 기초', '프로토타이핑', '애니메이션', '개발자 핸드오프']
            },
            {
                'title': 'Photoshop 그래픽 디자인',
                'slug': 'photoshop-graphic-design',
                'category': 'design',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '포토샵으로 전문가 되기',
                'description': 'Photoshop의 고급 기능을 활용한 그래픽 디자인을 마스터합니다.',
                'objectives': ['Photoshop 고급', '합성 기술', '레이어 마스터', '실전 프로젝트']
            },
            {
                'title': 'Illustrator 벡터 디자인',
                'slug': 'illustrator-vector-design',
                'category': 'design',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '일러스트레이터 완벽 마스터',
                'description': '일러스트레이터로 로고, 아이콘, 일러스트를 제작합니다.',
                'objectives': ['벡터 기초', '펜 툴 마스터', '타이포그래피', '브랜딩 디자인']
            },
            {
                'title': '3D 디자인 with Blender',
                'slug': '3d-design-blender',
                'category': 'design',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 129000,
                'short_description': 'Blender로 3D 모델링',
                'description': 'Blender를 활용한 3D 모델링과 렌더링을 배웁니다.',
                'objectives': ['3D 모델링', '텍스처링', '라이팅', '애니메이션']
            },
            {
                'title': '모션 그래픽 with After Effects',
                'slug': 'motion-graphics-ae',
                'category': 'design',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 99000,
                'short_description': 'After Effects 애니메이션',
                'description': 'After Effects로 전문가 수준의 모션 그래픽을 제작합니다.',
                'objectives': ['AE 기초', '키프레임', '이펙트', '실전 프로젝트']
            },

            # 비즈니스 & 마케팅 (33-40)
            {
                'title': '디지털 마케팅 완벽 가이드',
                'slug': 'digital-marketing-complete',
                'category': 'marketing',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 89000,
                'short_description': 'SEO부터 SNS 마케팅까지',
                'description': '디지털 마케팅의 모든 채널을 마스터합니다.',
                'objectives': ['SEO 최적화', 'SNS 마케팅', '콘텐츠 전략', 'GA4 분석']
            },
            {
                'title': 'Google Ads 광고 마스터',
                'slug': 'google-ads-master',
                'category': 'marketing',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '구글 광고로 성과 내기',
                'description': 'Google Ads를 활용한 효과적인 광고 캠페인을 운영합니다.',
                'objectives': ['검색 광고', '디스플레이 광고', '리마케팅', 'ROI 최적화']
            },
            {
                'title': 'Facebook & Instagram 광고',
                'slug': 'facebook-instagram-ads',
                'category': 'marketing',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 89000,
                'short_description': 'Meta 광고 완벽 마스터',
                'description': 'Facebook과 Instagram 광고로 비즈니스를 성장시킵니다.',
                'objectives': ['Meta 광고', '타겟팅 전략', 'A/B 테스팅', '광고 최적화']
            },
            {
                'title': '유튜브 채널 성장 전략',
                'slug': 'youtube-channel-growth',
                'category': 'marketing',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '유튜브로 수익 창출하기',
                'description': '유튜브 채널을 성공적으로 운영하는 모든 방법을 배웁니다.',
                'objectives': ['콘텐츠 기획', 'SEO 최적화', '수익화 전략', '편집 기술']
            },
            {
                'title': '이커머스 창업 완벽 가이드',
                'slug': 'ecommerce-startup-guide',
                'category': 'business',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '온라인 쇼핑몰 성공 전략',
                'description': '스마트스토어부터 쿠팡까지 이커머스 창업을 완벽하게 준비합니다.',
                'objectives': ['쇼핑몰 구축', '상품 소싱', '마케팅 전략', 'CS 관리']
            },
            {
                'title': '블로그 수익화 전략',
                'slug': 'blog-monetization',
                'category': 'marketing',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 69000,
                'short_description': '블로그로 월 100만원 벌기',
                'description': '블로그를 통한 애드센스, 제휴 마케팅 수익화를 배웁니다.',
                'objectives': ['블로그 SEO', '애드센스', '제휴 마케팅', '콘텐츠 전략']
            },
            {
                'title': 'Excel 데이터 분석 실무',
                'slug': 'excel-data-analysis',
                'category': 'business',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 59000,
                'short_description': '엑셀로 업무 자동화',
                'description': 'Excel의 고급 기능으로 업무 효율을 극대화합니다.',
                'objectives': ['피벗 테이블', '수식과 함수', 'VBA 매크로', '대시보드']
            },
            {
                'title': 'PowerPoint 프레젠테이션 마스터',
                'slug': 'powerpoint-master',
                'category': 'business',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '설득력 있는 PT 만들기',
                'description': 'PowerPoint로 전문가 수준의 프레젠테이션을 제작합니다.',
                'objectives': ['디자인 원칙', '애니메이션', '스토리텔링', '발표 기술']
            },

            # 언어 학습 (41-45)
            {
                'title': '왕초보 영어회화',
                'slug': 'english-conversation-beginner',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '기초 영어회화 30일 완성',
                'description': '영어 왕초보도 30일이면 기본 회화가 가능합니다.',
                'objectives': ['기초 문법', '필수 단어', '실전 회화', '발음 교정']
            },
            {
                'title': '비즈니스 영어 마스터',
                'slug': 'business-english-master',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '글로벌 비즈니스 영어',
                'description': '비즈니스 현장에서 바로 쓰는 실전 영어를 마스터합니다.',
                'objectives': ['이메일 작성', '미팅 영어', '프레젠테이션', '협상 영어']
            },
            {
                'title': '일본어 JLPT N2 완성',
                'slug': 'japanese-jlpt-n2',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 89000,
                'short_description': 'JLPT N2 한 번에 합격',
                'description': 'JLPT N2 시험을 체계적으로 준비합니다.',
                'objectives': ['N2 문법', '한자 800자', '청해 연습', '모의고사']
            },
            {
                'title': '중국어 HSK 6급 완성',
                'slug': 'chinese-hsk6',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 99000,
                'short_description': 'HSK 6급 완벽 대비',
                'description': 'HSK 6급 시험을 완벽하게 준비합니다.',
                'objectives': ['고급 문법', '어휘 5000개', '독해/작문', '모의고사']
            },
            {
                'title': '스페인어 기초 완성',
                'slug': 'spanish-basics',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 69000,
                'short_description': '스페인어 왕초보 탈출',
                'description': '스페인어의 기초를 탄탄하게 다집니다.',
                'objectives': ['기초 문법', '필수 어휘', '발음 연습', '간단한 회화']
            },

            # 기타 전문 분야 (46-50)
            {
                'title': 'AWS 클라우드 아키텍트',
                'slug': 'aws-cloud-architect',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 149000,
                'short_description': 'AWS 자격증 대비 완벽 가이드',
                'description': 'AWS 솔루션 아키텍트 자격증을 준비하고 실전 경험을 쌓습니다.',
                'objectives': ['AWS 핵심 서비스', 'EC2/S3/RDS', '보안/네트워킹', '자격증 대비']
            },
            {
                'title': 'Docker & Kubernetes 마스터',
                'slug': 'docker-kubernetes',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 119000,
                'short_description': '컨테이너 오케스트레이션 완벽 가이드',
                'description': 'Docker와 Kubernetes로 현대적인 인프라를 구축합니다.',
                'objectives': ['Docker 기초', 'Kubernetes', 'CI/CD', 'MSA 구축']
            },
            {
                'title': '블록체인 개발 입문',
                'slug': 'blockchain-development',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 139000,
                'short_description': 'Solidity로 스마트 컨트랙트 개발',
                'description': '블록체인의 원리부터 스마트 컨트랙트 개발까지 마스터합니다.',
                'objectives': ['블록체인 기초', 'Solidity', '스마트 컨트랙트', 'DApp 개발']
            },
            {
                'title': '사이버 보안 전문가',
                'slug': 'cybersecurity-expert',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 159000,
                'short_description': '화이트 해커 양성 과정',
                'description': '사이버 보안의 모든 것을 배우고 전문가가 됩니다.',
                'objectives': ['네트워크 보안', '웹 해킹', '모의 해킹', '보안 솔루션']
            },
            {
                'title': '게임 개발 with Unity',
                'slug': 'game-dev-unity',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 119000,
                'short_description': 'Unity로 2D/3D 게임 만들기',
                'description': 'Unity 엔진으로 완성도 높은 게임을 제작합니다.',
                'objectives': ['Unity 기초', 'C# 스크립팅', '게임 로직', '배포 및 수익화']
            },
        ]

        created_count = 0
        for idx, course_data in enumerate(courses_data):
            if Course.objects.filter(slug=course_data['slug']).exists():
                continue

            # Get random instructor
            instructor = random.choice(instructors)

            # Extract and remove objectives
            objectives = course_data.pop('objectives')
            price = course_data.pop('price', 0)

            # Create course
            course = Course.objects.create(
                instructor=instructor,
                price=price,
                is_published=True,
                total_enrollments=random.randint(50, 5000),
                average_rating=round(random.uniform(4.0, 5.0), 1),
                rating_count=random.randint(10, 1000),
                total_duration_minutes=random.randint(180, 1200),
                **course_data
            )
            course.learning_objectives = objectives
            course.save()

            # Create modules
            module_titles = [
                '시작하기',
                '기초 다지기',
                '핵심 개념',
                '실전 응용',
                '프로젝트'
            ]

            for mod_idx, mod_title in enumerate(module_titles[:random.randint(3, 5)]):
                module = Module.objects.create(
                    course=course,
                    title=mod_title,
                    description=f'{mod_title}에서 배울 내용들',
                    order=mod_idx
                )

                # Create lessons
                lesson_count = random.randint(3, 6)
                for les_idx in range(lesson_count):
                    lesson_types = ['video', 'text', 'quiz']
                    Lesson.objects.create(
                        module=module,
                        title=f'레슨 {les_idx + 1}',
                        lesson_type=random.choice(lesson_types),
                        content=f'{mod_title}의 {les_idx + 1}번째 레슨 내용입니다.',
                        order=les_idx,
                        is_preview=(les_idx == 0),
                        video_duration=random.randint(300, 1800)
                    )

            # Create practice questions
            for _ in range(random.randint(3, 8)):
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
            self.stdout.write(f'  ✅ [{created_count}/50] {course.title}')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 {created_count}개의 코스가 생성되었습니다!'))
