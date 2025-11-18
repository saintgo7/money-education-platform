"""
100개의 코스 데이터를 fixtures JSON 파일로 생성하는 스크립트
각 코스는 10-15개의 모듈과 각 모듈당 8-12개의 레슨을 포함
Django 없이 실행 가능
"""
import json
import random
from datetime import datetime, timedelta


def generate_courses_fixtures():
    """100개의 코스 fixtures 생성 (각 코스당 10-15개 모듈)"""

    # 강사 데이터 (15명으로 확장)
    instructors = []
    instructor_data = [
        ('김민수', 'minsu'), ('이지은', 'jieun'), ('박준호', 'junho'),
        ('최서연', 'seoyeon'), ('정대현', 'daehyun'), ('강하늘', 'haneul'),
        ('송지아', 'jia'), ('윤성호', 'seongho'), ('한소희', 'sohee'),
        ('임영웅', 'youngwoong'), ('안유진', 'yujin'), ('차은우', 'eunwoo'),
        ('전지현', 'jihyun'), ('이병헌', 'byunghun'), ('박보검', 'bogum'),
    ]

    user_pk = 1
    for idx, (name, username) in enumerate(instructor_data, 1):
        instructors.append({
            "model": "users.user",
            "pk": user_pk,
            "fields": {
                "username": username,
                "email": f"{username}@example.com",
                "first_name": name.split()[0],
                "last_name": name.split()[1] if len(name.split()) > 1 else "",
                "user_type": "instructor",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "date_joined": datetime.now().isoformat(),
            }
        })
        user_pk += 1

    # 100개의 코스 데이터
    courses_data = [
        # 금융 카테고리 (20개)
        {'title': '초보자를 위한 주식 투자 입문', 'category': 'finance', 'difficulty': 'beginner', 'short_description': '주식 시장의 기초부터 첫 투자까지', 'price': 49000},
        {'title': '부동산 투자 완벽 가이드', 'category': 'finance', 'difficulty': 'intermediate', 'short_description': '부동산 시장 분석부터 투자 전략까지', 'price': 89000},
        {'title': '암호화폐와 블록체인 투자', 'category': 'finance', 'difficulty': 'intermediate', 'short_description': '비트코인부터 DeFi까지 완벽 이해', 'price': 69000},
        {'title': '재무제표 읽는 법', 'category': 'finance', 'difficulty': 'beginner', 'short_description': '숫자로 기업 가치 파악하기', 'price': 39000},
        {'title': '퀀트 투자 전략 마스터', 'category': 'finance', 'difficulty': 'advanced', 'short_description': '데이터 기반 투자 전략 수립', 'price': 129000},
        {'title': '개인 재무관리와 자산 배분', 'category': 'finance', 'difficulty': 'beginner', 'short_description': '돈 모으는 습관부터 포트폴리오까지', 'price': 29000},
        {'title': 'ETF 투자 완벽 가이드', 'category': 'finance', 'difficulty': 'beginner', 'short_description': '분산 투자로 안정적 수익 창출', 'price': 49000},
        {'title': '채권 투자와 금리 분석', 'category': 'finance', 'difficulty': 'intermediate', 'short_description': '안정적 수익을 위한 채권 투자', 'price': 59000},
        {'title': '파생상품과 헤지 전략', 'category': 'finance', 'difficulty': 'advanced', 'short_description': '옵션, 선물로 위험 관리하기', 'price': 149000},
        {'title': '세금 절세 전략', 'category': 'finance', 'difficulty': 'intermediate', 'short_description': '합법적으로 세금 줄이는 방법', 'price': 79000},
        {'title': '가치투자의 원칙', 'category': 'finance', 'difficulty': 'intermediate', 'short_description': '워렌 버핏의 투자 철학 배우기', 'price': 89000},
        {'title': '기술적 분석 완벽 마스터', 'category': 'finance', 'difficulty': 'advanced', 'short_description': '차트와 지표로 매매 타이밍 잡기', 'price': 119000},
        {'title': '국내외 경제 지표 분석', 'category': 'finance', 'difficulty': 'intermediate', 'short_description': '거시경제 이해하고 투자에 활용', 'price': 69000},
        {'title': '연금과 노후 설계', 'category': 'finance', 'difficulty': 'beginner', 'short_description': '은퇴 후 안정적 삶을 위한 준비', 'price': 59000},
        {'title': '해외 주식 투자 가이드', 'category': 'finance', 'difficulty': 'intermediate', 'short_description': '미국, 중국 주식 시장 완벽 정복', 'price': 79000},
        {'title': '신용과 대출 관리', 'category': 'finance', 'difficulty': 'beginner', 'short_description': '똑똑하게 빌리고 갚는 법', 'price': 39000},
        {'title': '배당주 투자 전략', 'category': 'finance', 'difficulty': 'intermediate', 'short_description': '안정적 현금흐름 만들기', 'price': 69000},
        {'title': '리츠(REITs) 투자', 'category': 'finance', 'difficulty': 'intermediate', 'short_description': '부동산에 간접 투자하는 법', 'price': 59000},
        {'title': '스타트업 투자와 벤처캐피탈', 'category': 'finance', 'difficulty': 'advanced', 'short_description': '초기 기업 투자로 고수익 노리기', 'price': 139000},
        {'title': '보험과 리스크 관리', 'category': 'finance', 'difficulty': 'beginner', 'short_description': '나와 가족을 지키는 보험 설계', 'price': 49000},

        # 프로그래밍 카테고리 (20개)
        {'title': 'Python 기초부터 실전까지', 'category': 'programming', 'difficulty': 'beginner', 'short_description': '프로그래밍 입문자를 위한 파이썬', 'price': 59000},
        {'title': 'JavaScript 완벽 마스터', 'category': 'programming', 'difficulty': 'intermediate', 'short_description': '모던 JavaScript ES6+', 'price': 69000},
        {'title': 'React로 만드는 현대적 웹앱', 'category': 'programming', 'difficulty': 'intermediate', 'short_description': 'React Hooks와 Context API', 'price': 89000},
        {'title': 'Node.js 백엔드 개발', 'category': 'programming', 'difficulty': 'intermediate', 'short_description': 'Express와 MongoDB로 API 구축', 'price': 99000},
        {'title': 'Django로 만드는 풀스택 웹서비스', 'category': 'programming', 'difficulty': 'advanced', 'short_description': 'Python 웹 프레임워크 마스터', 'price': 129000},
        {'title': 'SQL 데이터베이스 완벽 가이드', 'category': 'programming', 'difficulty': 'beginner', 'short_description': '데이터베이스 설계부터 쿼리까지', 'price': 49000},
        {'title': 'Git과 GitHub 협업 실무', 'category': 'programming', 'difficulty': 'beginner', 'short_description': '버전 관리와 팀 협업', 'price': 29000},
        {'title': 'Docker와 Kubernetes 입문', 'category': 'programming', 'difficulty': 'advanced', 'short_description': '컨테이너 기반 배포 자동화', 'price': 149000},
        {'title': 'AWS 클라우드 아키텍처', 'category': 'programming', 'difficulty': 'advanced', 'short_description': '클라우드 인프라 설계와 구축', 'price': 179000},
        {'title': '알고리즘과 자료구조', 'category': 'programming', 'difficulty': 'intermediate', 'short_description': '코딩 테스트 완벽 대비', 'price': 79000},
        {'title': 'TypeScript 마스터클래스', 'category': 'programming', 'difficulty': 'intermediate', 'short_description': '타입 안정성으로 버그 줄이기', 'price': 79000},
        {'title': 'Vue.js 3 완벽 가이드', 'category': 'programming', 'difficulty': 'intermediate', 'short_description': 'Composition API로 반응형 앱 만들기', 'price': 89000},
        {'title': 'Spring Boot 백엔드', 'category': 'programming', 'difficulty': 'advanced', 'short_description': 'Java로 엔터프라이즈 애플리케이션 개발', 'price': 129000},
        {'title': 'Flutter 모바일 앱 개발', 'category': 'programming', 'difficulty': 'intermediate', 'short_description': '크로스 플랫폼 앱 한 번에', 'price': 99000},
        {'title': 'GraphQL API 설계', 'category': 'programming', 'difficulty': 'advanced', 'short_description': '유연한 API 구축하기', 'price': 119000},
        {'title': 'Redis와 캐싱 전략', 'category': 'programming', 'difficulty': 'advanced', 'short_description': '성능 최적화의 핵심', 'price': 89000},
        {'title': 'CI/CD 파이프라인 구축', 'category': 'programming', 'difficulty': 'advanced', 'short_description': '자동화된 배포 시스템', 'price': 139000},
        {'title': 'Linux 시스템 관리', 'category': 'programming', 'difficulty': 'intermediate', 'short_description': '서버 운영의 기초', 'price': 69000},
        {'title': '마이크로서비스 아키텍처', 'category': 'programming', 'difficulty': 'advanced', 'short_description': '확장 가능한 서비스 설계', 'price': 159000},
        {'title': 'Rust 프로그래밍', 'category': 'programming', 'difficulty': 'advanced', 'short_description': '안전하고 빠른 시스템 프로그래밍', 'price': 139000},

        # 데이터 사이언스 카테고리 (20개)
        {'title': '데이터 분석 입문 with Python', 'category': 'data_science', 'difficulty': 'beginner', 'short_description': 'Pandas와 NumPy로 시작하기', 'price': 69000},
        {'title': '머신러닝 완벽 가이드', 'category': 'data_science', 'difficulty': 'intermediate', 'short_description': 'Scikit-learn으로 배우는 ML', 'price': 119000},
        {'title': '딥러닝과 인공신경망', 'category': 'data_science', 'difficulty': 'advanced', 'short_description': 'TensorFlow와 PyTorch', 'price': 159000},
        {'title': '데이터 시각화 마스터', 'category': 'data_science', 'difficulty': 'beginner', 'short_description': 'Matplotlib, Seaborn, Plotly', 'price': 49000},
        {'title': 'SQL for Data Analysis', 'category': 'data_science', 'difficulty': 'intermediate', 'short_description': '데이터 분석을 위한 고급 SQL', 'price': 59000},
        {'title': '자연어 처리 NLP 실전', 'category': 'data_science', 'difficulty': 'advanced', 'short_description': 'BERT, GPT 활용하기', 'price': 169000},
        {'title': '통계학으로 배우는 데이터 분석', 'category': 'data_science', 'difficulty': 'intermediate', 'short_description': '확률과 통계의 실전 적용', 'price': 79000},
        {'title': 'A/B 테스트와 실험 설계', 'category': 'data_science', 'difficulty': 'intermediate', 'short_description': '데이터 기반 의사결정', 'price': 89000},
        {'title': '추천 시스템 구축하기', 'category': 'data_science', 'difficulty': 'advanced', 'short_description': '협업 필터링과 딥러닝', 'price': 149000},
        {'title': '시계열 데이터 분석', 'category': 'data_science', 'difficulty': 'intermediate', 'short_description': 'ARIMA, Prophet으로 예측하기', 'price': 99000},
        {'title': '컴퓨터 비전 CNN', 'category': 'data_science', 'difficulty': 'advanced', 'short_description': '이미지 인식과 객체 탐지', 'price': 149000},
        {'title': 'BigQuery로 빅데이터 분석', 'category': 'data_science', 'difficulty': 'intermediate', 'short_description': '대규모 데이터 처리', 'price': 89000},
        {'title': 'Tableau 데이터 시각화', 'category': 'data_science', 'difficulty': 'beginner', 'short_description': 'BI 도구로 인사이트 발견', 'price': 69000},
        {'title': '강화학습 입문', 'category': 'data_science', 'difficulty': 'advanced', 'short_description': 'RL 알고리즘 이해하고 구현', 'price': 179000},
        {'title': 'Apache Spark 빅데이터', 'category': 'data_science', 'difficulty': 'advanced', 'short_description': '분산 데이터 처리', 'price': 139000},
        {'title': '데이터 엔지니어링 파이프라인', 'category': 'data_science', 'difficulty': 'advanced', 'short_description': 'ETL과 데이터 웨어하우스', 'price': 149000},
        {'title': 'Feature Engineering', 'category': 'data_science', 'difficulty': 'intermediate', 'short_description': 'ML 성능 향상의 핵심', 'price': 89000},
        {'title': 'MLOps 실전', 'category': 'data_science', 'difficulty': 'advanced', 'short_description': 'ML 모델 배포와 모니터링', 'price': 159000},
        {'title': '이상 탐지 Anomaly Detection', 'category': 'data_science', 'difficulty': 'advanced', 'short_description': '비정상 패턴 찾기', 'price': 129000},
        {'title': 'AutoML과 신경망 아키텍처 탐색', 'category': 'data_science', 'difficulty': 'advanced', 'short_description': '자동화된 모델 최적화', 'price': 169000},

        # 비즈니스 카테고리 (20개)
        {'title': '스타트업 창업 완벽 가이드', 'category': 'business', 'difficulty': 'beginner', 'short_description': '아이디어부터 투자 유치까지', 'price': 99000},
        {'title': '린 스타트업 방법론', 'category': 'business', 'difficulty': 'intermediate', 'short_description': '빠르게 검증하고 성장하기', 'price': 79000},
        {'title': '프로젝트 관리 실무', 'category': 'business', 'difficulty': 'intermediate', 'short_description': 'Agile과 Scrum 마스터', 'price': 89000},
        {'title': '비즈니스 모델 캔버스', 'category': 'business', 'difficulty': 'beginner', 'short_description': '성공하는 비즈니스 모델 설계', 'price': 59000},
        {'title': '데이터 기반 의사결정', 'category': 'business', 'difficulty': 'intermediate', 'short_description': 'KPI 설정과 성과 측정', 'price': 79000},
        {'title': '협상의 기술', 'category': 'business', 'difficulty': 'intermediate', 'short_description': 'Win-Win 협상 전략', 'price': 69000},
        {'title': '비즈니스 영어 커뮤니케이션', 'category': 'business', 'difficulty': 'intermediate', 'short_description': '글로벌 비즈니스를 위한 영어', 'price': 89000},
        {'title': '프레젠테이션 스킬', 'category': 'business', 'difficulty': 'beginner', 'short_description': '설득력 있는 발표 만들기', 'price': 49000},
        {'title': 'B2B 세일즈 전략', 'category': 'business', 'difficulty': 'advanced', 'short_description': '기업 고객 영업 마스터', 'price': 129000},
        {'title': '공급망 관리 SCM', 'category': 'business', 'difficulty': 'advanced', 'short_description': '효율적인 물류와 재고 관리', 'price': 119000},
        {'title': '리더십과 팀 빌딩', 'category': 'business', 'difficulty': 'intermediate', 'short_description': '효과적인 팀 관리', 'price': 89000},
        {'title': 'OKR 목표 관리', 'category': 'business', 'difficulty': 'intermediate', 'short_description': '조직 목표 정렬과 달성', 'price': 69000},
        {'title': '기업 회계와 재무 관리', 'category': 'business', 'difficulty': 'intermediate', 'short_description': '회계 기초부터 재무제표까지', 'price': 79000},
        {'title': '전략 경영', 'category': 'business', 'difficulty': 'advanced', 'short_description': '경쟁 우위 확보 전략', 'price': 139000},
        {'title': '조직 문화와 HR', 'category': 'business', 'difficulty': 'intermediate', 'short_description': '인재 채용과 조직 관리', 'price': 89000},
        {'title': '변화 관리 Change Management', 'category': 'business', 'difficulty': 'advanced', 'short_description': '조직 혁신 성공시키기', 'price': 119000},
        {'title': '법인 설립과 법무', 'category': 'business', 'difficulty': 'beginner', 'short_description': '사업자 등록부터 계약서까지', 'price': 69000},
        {'title': '고객 서비스 전략', 'category': 'business', 'difficulty': 'beginner', 'short_description': 'CS로 고객 만족도 높이기', 'price': 59000},
        {'title': '제품 관리 Product Management', 'category': 'business', 'difficulty': 'advanced', 'short_description': '성공하는 제품 만들기', 'price': 129000},
        {'title': '프랜차이즈 비즈니스', 'category': 'business', 'difficulty': 'intermediate', 'short_description': '가맹점 사업 시작하기', 'price': 99000},

        # 마케팅 카테고리 (20개)
        {'title': '디지털 마케팅 완벽 가이드', 'category': 'marketing', 'difficulty': 'beginner', 'short_description': 'SEO, SNS, 콘텐츠 마케팅', 'price': 79000},
        {'title': '퍼포먼스 마케팅 실전', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': 'Google Ads, Facebook Ads', 'price': 99000},
        {'title': 'SEO 최적화 전략', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': '검색 엔진 상위 노출의 비밀', 'price': 69000},
        {'title': '콘텐츠 마케팅 전략', 'category': 'marketing', 'difficulty': 'beginner', 'short_description': '가치 있는 콘텐츠로 고객 유치', 'price': 59000},
        {'title': 'SNS 마케팅 마스터', 'category': 'marketing', 'difficulty': 'beginner', 'short_description': '인스타그램, 유튜브 활용법', 'price': 49000},
        {'title': '브랜딩의 모든 것', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': '강력한 브랜드 만들기', 'price': 89000},
        {'title': '이메일 마케팅 실전', 'category': 'marketing', 'difficulty': 'beginner', 'short_description': '높은 전환율의 이메일 캠페인', 'price': 39000},
        {'title': 'Growth Hacking', 'category': 'marketing', 'difficulty': 'advanced', 'short_description': '빠른 성장을 위한 실험과 최적화', 'price': 129000},
        {'title': '구글 애널리틱스 GA4', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': '데이터로 마케팅 성과 측정', 'price': 69000},
        {'title': '바이럴 마케팅 전략', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': '입소문 나는 콘텐츠 만들기', 'price': 79000},
        {'title': '인플루언서 마케팅', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': '협업으로 브랜드 알리기', 'price': 89000},
        {'title': 'CRM 고객 관계 관리', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': '고객 데이터 활용 전략', 'price': 79000},
        {'title': '모바일 마케팅', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': '앱 마케팅과 ASO', 'price': 89000},
        {'title': '유튜브 크리에이터', 'category': 'marketing', 'difficulty': 'beginner', 'short_description': '채널 성장과 수익화', 'price': 69000},
        {'title': '라이브커머스 전략', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': '실시간 판매로 매출 올리기', 'price': 99000},
        {'title': '마케팅 자동화 Automation', 'category': 'marketing', 'difficulty': 'advanced', 'short_description': '효율적인 캠페인 운영', 'price': 119000},
        {'title': 'UX 라이팅', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': '사용자 경험을 개선하는 글쓰기', 'price': 69000},
        {'title': '리타게팅 광고 전략', 'category': 'marketing', 'difficulty': 'advanced', 'short_description': '재방문 유도로 전환율 높이기', 'price': 89000},
        {'title': '네이버 스마트스토어', 'category': 'marketing', 'difficulty': 'beginner', 'short_description': '온라인 쇼핑몰 시작하기', 'price': 59000},
        {'title': '브랜드 스토리텔링', 'category': 'marketing', 'difficulty': 'intermediate', 'short_description': '감성으로 연결하는 브랜드', 'price': 79000},
    ]

    fixtures = instructors.copy()
    course_pk = 1
    module_pk = 1
    lesson_pk = 1

    print(f"총 {len(courses_data)}개의 코스 생성 중...")

    for idx, course_data in enumerate(courses_data, 1):
        # 슬러그 생성
        slug = course_data['title'].lower().replace(' ', '-')

        # 할인가 랜덤 생성 (30%는 할인)
        discount_price = None
        if random.random() < 0.3:
            discount_price = int(course_data['price'] * 0.7)

        # 코스 fixture
        course_fixture = {
            "model": "courses.course",
            "pk": course_pk,
            "fields": {
                "title": course_data['title'],
                "slug": slug,
                "short_description": course_data['short_description'],
                "description": f"{course_data['title']}에서 배울 수 있는 내용을 체계적으로 학습합니다. 기초부터 실전까지 단계별로 구성된 커리큘럼을 통해 전문성을 키워보세요. 실무 프로젝트와 다양한 실습을 통해 실전 경험을 쌓을 수 있습니다.",
                "instructor": random.randint(1, len(instructor_data)),
                "category": course_data['category'],
                "difficulty": course_data['difficulty'],
                "price": str(course_data['price']),
                "discount_price": str(discount_price) if discount_price else None,
                "price_type": "paid",
                "is_published": True,
                "total_duration_minutes": random.randint(600, 2400),  # 10-40시간
                "total_enrollments": random.randint(50, 8000),
                "average_rating": f"{random.uniform(4.2, 5.0):.2f}",
                "rating_count": random.randint(20, 1200),
                "learning_objectives": [
                    f"{course_data['title']}의 핵심 개념과 원리 완벽 이해",
                    "실전 프로젝트를 통한 실무 능력 향상",
                    "업계 베스트 프랙티스와 최신 트렌드 학습",
                    "포트폴리오 제작 및 실무 적용 능력 배양",
                ],
                "prerequisites": "기초 지식이 있으면 도움이 되지만 필수는 아닙니다. 열정과 학습 의지만 있으면 누구나 수강 가능합니다.",
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
        }
        fixtures.append(course_fixture)

        # 각 코스에 모듈 생성 (10-15개)
        num_modules = random.randint(10, 15)
        for module_num in range(1, num_modules + 1):
            module_fixture = {
                "model": "courses.module",
                "pk": module_pk,
                "fields": {
                    "course": course_pk,
                    "title": f"모듈 {module_num}: {get_module_title(course_data['category'], module_num)}",
                    "description": f"이 모듈에서는 {course_data['title']}의 주요 개념과 실전 노하우를 단계별로 학습합니다.",
                    "order": module_num,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                }
            }
            fixtures.append(module_fixture)

            # 각 모듈에 레슨 생성 (8-12개)
            num_lessons = random.randint(8, 12)
            lesson_types = ['video', 'video', 'video', 'text', 'quiz', 'assignment']  # 비디오 비중 높임

            for lesson_num in range(1, num_lessons + 1):
                lesson_type = random.choice(lesson_types)
                is_preview = lesson_num == 1 and module_num == 1

                lesson_fixture = {
                    "model": "courses.lesson",
                    "pk": lesson_pk,
                    "fields": {
                        "module": module_pk,
                        "title": f"레슨 {lesson_num}: {get_lesson_title(lesson_type, module_num)}",
                        "lesson_type": lesson_type,
                        "order": lesson_num,
                        "content": f"이 레슨에서는 핵심 개념을 상세하게 다룹니다. 실습 예제와 함께 단계별로 학습하세요." if lesson_type == 'text' else "",
                        "video_url": f"https://example.com/videos/{slug}-m{module_num}-l{lesson_num}.mp4" if lesson_type == 'video' else "",
                        "video_duration": random.randint(600, 2400) if lesson_type == 'video' else 0,  # 10-40분
                        "is_preview": is_preview,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat(),
                    }
                }
                fixtures.append(lesson_fixture)
                lesson_pk += 1

            module_pk += 1

        course_pk += 1
        if idx % 10 == 0:
            print(f"  진행률: {idx}/100 코스 완료")

    return fixtures


def get_module_title(category, module_num):
    """카테고리와 모듈 번호에 따른 제목"""
    titles = {
        'finance': [
            '투자의 기초', '시장 분석', '포트폴리오 구성', '리스크 관리', '기술적 분석',
            '기본적 분석', '투자 심리', '세금 전략', '실전 투자', '고급 전략',
            '사례 연구', '시뮬레이션', '최신 트렌드', '전문가 인터뷰', '종합 정리'
        ],
        'programming': [
            '개발 환경 설정', '기본 문법', '핵심 개념', '자료구조', '알고리즘',
            '디자인 패턴', '데이터베이스', 'API 개발', '테스트', '배포',
            '성능 최적화', '보안', '실전 프로젝트', '코드 리뷰', '베스트 프랙티스'
        ],
        'data_science': [
            '데이터 수집', '데이터 전처리', '탐색적 분석', '시각화', '통계 분석',
            '특성 공학', '모델 선택', '모델 학습', '하이퍼파라미터 튜닝', '모델 평가',
            '교차 검증', '앙상블', '배포', '모니터링', '실전 프로젝트'
        ],
        'business': [
            '비즈니스 기초', '시장 조사', '전략 수립', '실행 계획', '팀 구성',
            '자금 조달', '마케팅', '세일즈', '운영 관리', '성과 측정',
            '스케일링', '파트너십', '위기 관리', '사례 연구', '성공 전략'
        ],
        'marketing': [
            '마케팅 기초', '타겟 고객 분석', '콘텐츠 전략', '채널 선택', '캠페인 기획',
            '광고 운영', '소셜 미디어', 'SEO/SEM', '데이터 분석', 'A/B 테스트',
            '전환 최적화', '리타게팅', '브랜딩', '성과 측정', '고급 전략'
        ],
    }
    category_titles = titles.get(category, ['기본', '중급', '고급', '심화', '실전'] * 3)
    return category_titles[min(module_num - 1, len(category_titles) - 1)]


def get_lesson_title(lesson_type, module_num):
    """레슨 타입별 제목"""
    titles = {
        'video': [
            '핵심 개념 강의', '실습 따라하기', '심화 학습', '사례 분석',
            '전문가 인터뷰', '실무 노하우', '트러블슈팅', '최신 트렌드',
            '베스트 프랙티스', '코드 리뷰', '라이브 코딩', '프로젝트 구현'
        ],
        'text': [
            '이론 학습', '개념 정리', '참고 자료', '가이드라인',
            '체크리스트', '용어 정리', '심화 자료', 'FAQ'
        ],
        'quiz': [
            '이해도 체크', '실력 테스트', '종합 퀴즈', '복습 문제',
            '실전 문제', '모의고사', '챌린지', '마스터 테스트'
        ],
        'assignment': [
            '실전 과제', '프로젝트 실습', '케이스 스터디', '포트폴리오',
            '미니 프로젝트', '팀 프로젝트', '캡스톤', '최종 프로젝트'
        ],
    }
    type_titles = titles.get(lesson_type, ['학습 자료'])
    return random.choice(type_titles)


if __name__ == '__main__':
    print("=" * 60)
    print("100개 코스 fixtures 생성 스크립트")
    print("각 코스는 10-15개 모듈, 각 모듈은 8-12개 레슨 포함")
    print("=" * 60)
    print()

    fixtures = generate_courses_fixtures()

    output_file = 'courses_fixtures.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixtures, f, ensure_ascii=False, indent=2)

    print()
    print("=" * 60)
    print(f"✓ {output_file} 파일 생성 완료!")
    print("=" * 60)
    print(f"📊 생성 통계:")
    print(f"  - 총 {len([f for f in fixtures if f['model'] == 'users.user'])}명 강사")
    print(f"  - 총 {len([f for f in fixtures if f['model'] == 'courses.course'])}개 코스")
    print(f"  - 총 {len([f for f in fixtures if f['model'] == 'courses.module'])}개 모듈")
    print(f"  - 총 {len([f for f in fixtures if f['model'] == 'courses.lesson'])}개 레슨")
    print()
    print("💾 파일 크기:", f"{len(json.dumps(fixtures)) / 1024 / 1024:.2f} MB")
    print()
    print("🚀 사용 방법:")
    print("  python manage.py loaddata courses_fixtures.json")
    print("=" * 60)
