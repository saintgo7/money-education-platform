"""
50개의 코스 데이터를 fixtures JSON 파일로 생성하는 스크립트
Django 없이 실행 가능
"""
import json
import random
from datetime import datetime, timedelta


def generate_courses_fixtures():
    """50개의 코스 fixtures 생성"""

    # 강사 데이터 (8명)
    instructors = []
    instructor_data = [
        ('김민수', 'minsu'),
        ('이지은', 'jieun'),
        ('박준호', 'junho'),
        ('최서연', 'seoyeon'),
        ('정대현', 'daehyun'),
        ('강하늘', 'haneul'),
        ('송지아', 'jia'),
        ('윤성호', 'seongho'),
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

    # 코스 데이터
    courses_data = [
        # 금융 (10개)
        {'title': '초보자를 위한 주식 투자 입문', 'category': 'finance', 'difficulty': 'beginner',
         'short_description': '주식 시장의 기초부터 첫 투자까지', 'price': 49000},
        {'title': '부동산 투자 완벽 가이드', 'category': 'finance', 'difficulty': 'intermediate',
         'short_description': '부동산 시장 분석부터 투자 전략까지', 'price': 89000},
        {'title': '암호화폐와 블록체인 투자', 'category': 'finance', 'difficulty': 'intermediate',
         'short_description': '비트코인부터 DeFi까지 완벽 이해', 'price': 69000},
        {'title': '재무제표 읽는 법', 'category': 'finance', 'difficulty': 'beginner',
         'short_description': '숫자로 기업 가치 파악하기', 'price': 39000},
        {'title': '퀀트 투자 전략 마스터', 'category': 'finance', 'difficulty': 'advanced',
         'short_description': '데이터 기반 투자 전략 수립', 'price': 129000},
        {'title': '개인 재무관리와 자산 배분', 'category': 'finance', 'difficulty': 'beginner',
         'short_description': '돈 모으는 습관부터 포트폴리오까지', 'price': 29000},
        {'title': 'ETF 투자 완벽 가이드', 'category': 'finance', 'difficulty': 'beginner',
         'short_description': '분산 투자로 안정적 수익 창출', 'price': 49000},
        {'title': '채권 투자와 금리 분석', 'category': 'finance', 'difficulty': 'intermediate',
         'short_description': '안정적 수익을 위한 채권 투자', 'price': 59000},
        {'title': '파생상품과 헤지 전략', 'category': 'finance', 'difficulty': 'advanced',
         'short_description': '옵션, 선물로 위험 관리하기', 'price': 149000},
        {'title': '세금 절세 전략', 'category': 'finance', 'difficulty': 'intermediate',
         'short_description': '합법적으로 세금 줄이는 방법', 'price': 79000},

        # 프로그래밍 (10개)
        {'title': 'Python 기초부터 실전까지', 'category': 'programming', 'difficulty': 'beginner',
         'short_description': '프로그래밍 입문자를 위한 파이썬', 'price': 59000},
        {'title': 'JavaScript 완벽 마스터', 'category': 'programming', 'difficulty': 'intermediate',
         'short_description': '모던 JavaScript ES6+', 'price': 69000},
        {'title': 'React로 만드는 현대적 웹앱', 'category': 'programming', 'difficulty': 'intermediate',
         'short_description': 'React Hooks와 Context API', 'price': 89000},
        {'title': 'Node.js 백엔드 개발', 'category': 'programming', 'difficulty': 'intermediate',
         'short_description': 'Express와 MongoDB로 API 구축', 'price': 99000},
        {'title': 'Django로 만드는 풀스택 웹서비스', 'category': 'programming', 'difficulty': 'advanced',
         'short_description': 'Python 웹 프레임워크 마스터', 'price': 129000},
        {'title': 'SQL 데이터베이스 완벽 가이드', 'category': 'programming', 'difficulty': 'beginner',
         'short_description': '데이터베이스 설계부터 쿼리까지', 'price': 49000},
        {'title': 'Git과 GitHub 협업 실무', 'category': 'programming', 'difficulty': 'beginner',
         'short_description': '버전 관리와 팀 협업', 'price': 29000},
        {'title': 'Docker와 Kubernetes 입문', 'category': 'programming', 'difficulty': 'advanced',
         'short_description': '컨테이너 기반 배포 자동화', 'price': 149000},
        {'title': 'AWS 클라우드 아키텍처', 'category': 'programming', 'difficulty': 'advanced',
         'short_description': '클라우드 인프라 설계와 구축', 'price': 179000},
        {'title': '알고리즘과 자료구조', 'category': 'programming', 'difficulty': 'intermediate',
         'short_description': '코딩 테스트 완벽 대비', 'price': 79000},

        # 데이터 사이언스 (10개)
        {'title': '데이터 분석 입문 with Python', 'category': 'data_science', 'difficulty': 'beginner',
         'short_description': 'Pandas와 NumPy로 시작하기', 'price': 69000},
        {'title': '머신러닝 완벽 가이드', 'category': 'data_science', 'difficulty': 'intermediate',
         'short_description': 'Scikit-learn으로 배우는 ML', 'price': 119000},
        {'title': '딥러닝과 인공신경망', 'category': 'data_science', 'difficulty': 'advanced',
         'short_description': 'TensorFlow와 PyTorch', 'price': 159000},
        {'title': '데이터 시각화 마스터', 'category': 'data_science', 'difficulty': 'beginner',
         'short_description': 'Matplotlib, Seaborn, Plotly', 'price': 49000},
        {'title': 'SQL for Data Analysis', 'category': 'data_science', 'difficulty': 'intermediate',
         'short_description': '데이터 분석을 위한 고급 SQL', 'price': 59000},
        {'title': '자연어 처리 NLP 실전', 'category': 'data_science', 'difficulty': 'advanced',
         'short_description': 'BERT, GPT 활용하기', 'price': 169000},
        {'title': '통계학으로 배우는 데이터 분석', 'category': 'data_science', 'difficulty': 'intermediate',
         'short_description': '확률과 통계의 실전 적용', 'price': 79000},
        {'title': 'A/B 테스트와 실험 설계', 'category': 'data_science', 'difficulty': 'intermediate',
         'short_description': '데이터 기반 의사결정', 'price': 89000},
        {'title': '추천 시스템 구축하기', 'category': 'data_science', 'difficulty': 'advanced',
         'short_description': '협업 필터링과 딥러닝', 'price': 149000},
        {'title': '시계열 데이터 분석', 'category': 'data_science', 'difficulty': 'intermediate',
         'short_description': 'ARIMA, Prophet으로 예측하기', 'price': 99000},

        # 비즈니스 (10개)
        {'title': '스타트업 창업 완벽 가이드', 'category': 'business', 'difficulty': 'beginner',
         'short_description': '아이디어부터 투자 유치까지', 'price': 99000},
        {'title': '린 스타트업 방법론', 'category': 'business', 'difficulty': 'intermediate',
         'short_description': '빠르게 검증하고 성장하기', 'price': 79000},
        {'title': '프로젝트 관리 실무', 'category': 'business', 'difficulty': 'intermediate',
         'short_description': 'Agile과 Scrum 마스터', 'price': 89000},
        {'title': '비즈니스 모델 캔버스', 'category': 'business', 'difficulty': 'beginner',
         'short_description': '성공하는 비즈니스 모델 설계', 'price': 59000},
        {'title': '데이터 기반 의사결정', 'category': 'business', 'difficulty': 'intermediate',
         'short_description': 'KPI 설정과 성과 측정', 'price': 79000},
        {'title': '협상의 기술', 'category': 'business', 'difficulty': 'intermediate',
         'short_description': 'Win-Win 협상 전략', 'price': 69000},
        {'title': '비즈니스 영어 커뮤니케이션', 'category': 'business', 'difficulty': 'intermediate',
         'short_description': '글로벌 비즈니스를 위한 영어', 'price': 89000},
        {'title': '프레젠테이션 스킬', 'category': 'business', 'difficulty': 'beginner',
         'short_description': '설득력 있는 발표 만들기', 'price': 49000},
        {'title': 'B2B 세일즈 전략', 'category': 'business', 'difficulty': 'advanced',
         'short_description': '기업 고객 영업 마스터', 'price': 129000},
        {'title': '공급망 관리 SCM', 'category': 'business', 'difficulty': 'advanced',
         'short_description': '효율적인 물류와 재고 관리', 'price': 119000},

        # 마케팅 (10개)
        {'title': '디지털 마케팅 완벽 가이드', 'category': 'marketing', 'difficulty': 'beginner',
         'short_description': 'SEO, SNS, 콘텐츠 마케팅', 'price': 79000},
        {'title': '퍼포먼스 마케팅 실전', 'category': 'marketing', 'difficulty': 'intermediate',
         'short_description': 'Google Ads, Facebook Ads', 'price': 99000},
        {'title': 'SEO 최적화 전략', 'category': 'marketing', 'difficulty': 'intermediate',
         'short_description': '검색 엔진 상위 노출의 비밀', 'price': 69000},
        {'title': '콘텐츠 마케팅 전략', 'category': 'marketing', 'difficulty': 'beginner',
         'short_description': '가치 있는 콘텐츠로 고객 유치', 'price': 59000},
        {'title': 'SNS 마케팅 마스터', 'category': 'marketing', 'difficulty': 'beginner',
         'short_description': '인스타그램, 유튜브 활용법', 'price': 49000},
        {'title': '브랜딩의 모든 것', 'category': 'marketing', 'difficulty': 'intermediate',
         'short_description': '강력한 브랜드 만들기', 'price': 89000},
        {'title': '이메일 마케팅 실전', 'category': 'marketing', 'difficulty': 'beginner',
         'short_description': '높은 전환율의 이메일 캠페인', 'price': 39000},
        {'title': 'Growth Hacking', 'category': 'marketing', 'difficulty': 'advanced',
         'short_description': '빠른 성장을 위한 실험과 최적화', 'price': 129000},
        {'title': '구글 애널리틱스 GA4', 'category': 'marketing', 'difficulty': 'intermediate',
         'short_description': '데이터로 마케팅 성과 측정', 'price': 69000},
        {'title': '바이럴 마케팅 전략', 'category': 'marketing', 'difficulty': 'intermediate',
         'short_description': '입소문 나는 콘텐츠 만들기', 'price': 79000},
    ]

    fixtures = instructors.copy()
    course_pk = 1
    module_pk = 1
    lesson_pk = 1

    for course_data in courses_data:
        # 슬러그 생성 (간단한 버전)
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
                "description": f"{course_data['title']}에서 배울 수 있는 내용을 체계적으로 학습합니다. 기초부터 실전까지 단계별로 구성된 커리큘럼을 통해 전문성을 키워보세요.",
                "instructor": random.randint(1, len(instructor_data)),
                "category": course_data['category'],
                "difficulty": course_data['difficulty'],
                "price": str(course_data['price']),
                "discount_price": str(discount_price) if discount_price else None,
                "price_type": "paid",
                "is_published": True,
                "total_duration_minutes": random.randint(180, 1200),
                "total_enrollments": random.randint(10, 5000),
                "average_rating": f"{random.uniform(4.0, 5.0):.2f}",
                "rating_count": random.randint(5, 500),
                "learning_objectives": [
                    f"{course_data['title']}의 핵심 개념 이해",
                    "실전 프로젝트를 통한 실습",
                    "업계 베스트 프랙티스 학습",
                ],
                "prerequisites": "기초 지식이 있으면 좋지만 필수는 아닙니다.",
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
        }
        fixtures.append(course_fixture)

        # 각 코스에 모듈 생성 (3-6개)
        num_modules = random.randint(3, 5)
        for module_num in range(1, num_modules + 1):
            module_fixture = {
                "model": "courses.module",
                "pk": module_pk,
                "fields": {
                    "course": course_pk,
                    "title": f"모듈 {module_num}: {get_module_title(course_data['category'])}",
                    "description": f"이 모듈에서는 {course_data['title']}의 주요 개념을 배웁니다.",
                    "order": module_num,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                }
            }
            fixtures.append(module_fixture)

            # 각 모듈에 레슨 생성 (4-8개)
            num_lessons = random.randint(4, 7)
            lesson_types = ['video', 'text', 'quiz', 'assignment']

            for lesson_num in range(1, num_lessons + 1):
                lesson_type = random.choice(lesson_types)
                is_preview = lesson_num == 1 and module_num == 1

                lesson_fixture = {
                    "model": "courses.lesson",
                    "pk": lesson_pk,
                    "fields": {
                        "module": module_pk,
                        "title": f"레슨 {lesson_num}: {get_lesson_title(lesson_type)}",
                        "lesson_type": lesson_type,
                        "order": lesson_num,
                        "content": f"이 레슨의 내용입니다." if lesson_type == 'text' else "",
                        "video_url": f"https://example.com/videos/{slug}-{module_num}-{lesson_num}.mp4" if lesson_type == 'video' else "",
                        "video_duration": random.randint(300, 1800) if lesson_type == 'video' else 0,
                        "is_preview": is_preview,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat(),
                    }
                }
                fixtures.append(lesson_fixture)
                lesson_pk += 1

            module_pk += 1

        course_pk += 1

    return fixtures


def get_module_title(category):
    """카테고리별 모듈 제목"""
    titles = {
        'finance': ['기초 이론', '실전 전략', '사례 연구', '위험 관리', '고급 테크닉'],
        'programming': ['기본 문법', '핵심 개념', '실전 프로젝트', '최적화', '배포'],
        'data_science': ['데이터 전처리', '탐색적 분석', '모델 개발', '성능 평가', '실전 응용'],
        'business': ['기초 개념', '실전 전략', '사례 연구', '협업 도구', '심화 학습'],
        'marketing': ['마케팅 기초', '채널 전략', '캠페인 기획', '성과 분석', '고급 기법'],
    }
    return random.choice(titles.get(category, ['기본', '중급', '고급']))


def get_lesson_title(lesson_type):
    """레슨 타입별 제목"""
    titles = {
        'video': ['핵심 개념 강의', '실습 따라하기', '사례 분석', '전문가 인터뷰'],
        'text': ['이론 학습', '개념 정리', '가이드라인', '체크리스트'],
        'quiz': ['이해도 체크', '실력 테스트', '종합 퀴즈', '복습 문제'],
        'assignment': ['실전 과제', '프로젝트 실습', '케이스 스터디', '포트폴리오 만들기'],
    }
    return random.choice(titles.get(lesson_type, ['학습 자료']))


if __name__ == '__main__':
    print("코스 fixtures 생성 중...")
    fixtures = generate_courses_fixtures()

    output_file = 'courses_fixtures.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixtures, f, ensure_ascii=False, indent=2)

    print(f"✓ {output_file} 파일이 생성되었습니다!")
    print(f"  - 총 {len([f for f in fixtures if f['model'] == 'courses.course'])}개 코스")
    print(f"  - 총 {len([f for f in fixtures if f['model'] == 'courses.module'])}개 모듈")
    print(f"  - 총 {len([f for f in fixtures if f['model'] == 'courses.lesson'])}개 레슨")
    print(f"\n사용 방법:")
    print(f"  python manage.py loaddata {output_file}")
