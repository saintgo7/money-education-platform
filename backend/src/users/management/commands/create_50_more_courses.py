"""
Management command to create 50 additional diverse courses
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
from ai.models import PracticeQuestion
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create 50 additional diverse courses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating 50 additional courses...')

        # Get existing instructors or create new ones
        instructors = list(User.objects.filter(user_type='instructor'))

        if len(instructors) < 10:
            # Create more instructors
            additional_instructors = [
                ('Emily', 'Watson', 'AI/ML 전문가'),
                ('David', 'Chen', '클라우드 아키텍트'),
                ('Sarah', 'Kim', '디지털 마케팅 전문가'),
                ('Michael', 'Park', '게임 개발자'),
                ('Jessica', 'Lee', 'UX 디자이너'),
                ('Robert', 'Johnson', '금융 전문가'),
                ('Lisa', 'Wang', '건강 트레이너'),
                ('James', 'Brown', '음악 프로듀서'),
                ('Amanda', 'Martinez', '요리 전문가'),
                ('Chris', 'Taylor', '사진작가'),
            ]

            for idx, (first, last, bio) in enumerate(additional_instructors):
                username = f'instructor_new_{idx}'
                if not User.objects.filter(username=username).exists():
                    new_inst = User.objects.create_user(
                        username=username,
                        email=f'{username}@example.com',
                        password='instructor123',
                        first_name=first,
                        last_name=last,
                        user_type='instructor',
                        verified_instructor=True
                    )
                    instructors.append(new_inst)

        # 50 additional diverse courses
        courses_data = [
            # 고급 프로그래밍 (1-10)
            {
                'title': 'Rust 시스템 프로그래밍 마스터',
                'slug': 'rust-systems-programming',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 149000,
                'short_description': '안전하고 빠른 시스템 프로그래밍',
                'description': 'Rust로 고성능 시스템 소프트웨어를 개발합니다. 메모리 안전성과 동시성을 마스터하세요.',
                'objectives': ['Ownership 이해', 'Lifetime 관리', '안전한 동시성', '시스템 레벨 프로그래밍']
            },
            {
                'title': 'Kotlin 안드로이드 앱 개발 완성',
                'slug': 'kotlin-android-complete',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 129000,
                'short_description': 'Kotlin으로 만드는 현대적인 Android 앱',
                'description': 'Kotlin과 Jetpack Compose로 네이티브 Android 앱을 개발합니다.',
                'objectives': ['Kotlin 문법', 'Jetpack Compose', 'MVVM 아키텍처', 'Room 데이터베이스']
            },
            {
                'title': 'SwiftUI iOS 앱 개발',
                'slug': 'swiftui-ios-development',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 139000,
                'short_description': 'SwiftUI로 아름다운 iOS 앱 만들기',
                'description': 'SwiftUI를 활용한 선언형 iOS 앱 개발을 마스터합니다.',
                'objectives': ['SwiftUI 기초', 'Combine 프레임워크', 'CoreData', 'App Store 배포']
            },
            {
                'title': 'C# .NET 백엔드 개발',
                'slug': 'csharp-dotnet-backend',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 119000,
                'short_description': 'C#과 .NET으로 엔터프라이즈 백엔드',
                'description': 'ASP.NET Core로 확장 가능한 백엔드 시스템을 구축합니다.',
                'objectives': ['C# 고급 문법', 'ASP.NET Core', 'Entity Framework', 'Azure 배포']
            },
            {
                'title': 'Scala 함수형 프로그래밍',
                'slug': 'scala-functional-programming',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 159000,
                'short_description': '함수형 프로그래밍의 정수',
                'description': 'Scala로 함수형 프로그래밍 패러다임을 완벽하게 이해합니다.',
                'objectives': ['함수형 개념', 'Monad 이해', 'Akka 액터 모델', 'Spark 프로그래밍']
            },
            {
                'title': 'Elixir Phoenix 웹 개발',
                'slug': 'elixir-phoenix-web',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 139000,
                'short_description': '고가용성 실시간 웹 애플리케이션',
                'description': 'Elixir와 Phoenix로 확장 가능한 실시간 애플리케이션을 구축합니다.',
                'objectives': ['Elixir 기초', 'OTP 디자인', 'Phoenix Framework', 'LiveView']
            },
            {
                'title': 'Haskell 순수 함수형 프로그래밍',
                'slug': 'haskell-pure-functional',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 169000,
                'short_description': '순수 함수형 언어의 깊이',
                'description': 'Haskell로 수학적으로 엄밀한 프로그래밍을 학습합니다.',
                'objectives': ['Type System', 'Functor/Monad', 'Lazy Evaluation', '대수적 데이터 타입']
            },
            {
                'title': 'WebAssembly 고성능 웹 앱',
                'slug': 'webassembly-high-performance',
                'category': 'programming',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 149000,
                'short_description': 'WASM으로 웹의 성능 한계 돌파',
                'description': 'WebAssembly를 활용해 네이티브 수준의 웹 애플리케이션을 개발합니다.',
                'objectives': ['WASM 기초', 'Rust to WASM', 'JS 연동', '성능 최적화']
            },
            {
                'title': 'Flutter 크로스플랫폼 앱 개발 심화',
                'slug': 'flutter-advanced-crossplatform',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 139000,
                'short_description': 'Flutter로 iOS, Android, Web 동시 개발',
                'description': 'Flutter로 모든 플랫폼을 아우르는 아름다운 앱을 만듭니다.',
                'objectives': ['Flutter 고급', 'State Management', 'Native 통합', '앱 배포']
            },
            {
                'title': 'GraphQL API 설계와 구현',
                'slug': 'graphql-api-design',
                'category': 'programming',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 119000,
                'short_description': '차세대 API 아키텍처',
                'description': 'GraphQL로 효율적이고 유연한 API를 설계하고 구축합니다.',
                'objectives': ['GraphQL 스키마', 'Apollo Server', 'Resolver 패턴', 'N+1 문제 해결']
            },

            # 클라우드 & DevOps (11-20)
            {
                'title': 'AWS Solutions Architect 실전',
                'slug': 'aws-solutions-architect-practice',
                'category': 'cloud',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 199000,
                'short_description': 'AWS 아키텍트 자격증 + 실무',
                'description': 'AWS에서 확장 가능하고 안전한 인프라를 설계합니다.',
                'objectives': ['EC2/ECS/EKS', 'VPC 네트워킹', 'IAM 보안', '비용 최적화']
            },
            {
                'title': 'Google Cloud Platform 완벽 가이드',
                'slug': 'gcp-complete-guide',
                'category': 'cloud',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 179000,
                'short_description': 'GCP로 클라우드 네이티브 앱 구축',
                'description': 'Google Cloud의 모든 서비스를 활용한 애플리케이션 개발을 학습합니다.',
                'objectives': ['Compute Engine', 'Kubernetes Engine', 'BigQuery', 'Cloud Functions']
            },
            {
                'title': 'Azure DevOps 엔지니어',
                'slug': 'azure-devops-engineer',
                'category': 'cloud',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 169000,
                'short_description': 'Microsoft Azure CI/CD 파이프라인',
                'description': 'Azure DevOps로 완전 자동화된 배포 파이프라인을 구축합니다.',
                'objectives': ['Azure Pipelines', 'ARM Templates', 'Azure Monitor', 'DevTest Labs']
            },
            {
                'title': 'Terraform Infrastructure as Code',
                'slug': 'terraform-iac-mastery',
                'category': 'cloud',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 149000,
                'short_description': 'IaC로 인프라 자동화',
                'description': 'Terraform으로 멀티 클라우드 인프라를 코드로 관리합니다.',
                'objectives': ['HCL 문법', 'State 관리', 'Module 설계', '멀티 클라우드']
            },
            {
                'title': 'Jenkins CI/CD 파이프라인 구축',
                'slug': 'jenkins-cicd-pipeline',
                'category': 'cloud',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 129000,
                'short_description': 'Jenkins로 완전 자동화',
                'description': 'Jenkins를 활용한 엔터프라이즈급 CI/CD 파이프라인을 구축합니다.',
                'objectives': ['Jenkinsfile', 'Pipeline as Code', 'Blue-Green Deploy', '보안 스캔']
            },
            {
                'title': 'GitLab CI/CD 완벽 마스터',
                'slug': 'gitlab-cicd-complete',
                'category': 'cloud',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 119000,
                'short_description': 'GitLab으로 DevOps 완성',
                'description': 'GitLab CI/CD로 소스 관리부터 배포까지 통합 관리합니다.',
                'objectives': ['.gitlab-ci.yml', 'Runner 설정', 'Auto DevOps', 'Security Scanning']
            },
            {
                'title': 'Ansible 자동화 마스터',
                'slug': 'ansible-automation-master',
                'category': 'cloud',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 139000,
                'short_description': 'Ansible로 인프라 자동화',
                'description': 'Ansible Playbook으로 수백 대의 서버를 자동으로 관리합니다.',
                'objectives': ['Playbook 작성', 'Role 설계', 'Inventory 관리', 'Vault 암호화']
            },
            {
                'title': 'Kubernetes 운영 실무',
                'slug': 'kubernetes-operations',
                'category': 'cloud',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 189000,
                'short_description': 'K8s 클러스터 운영 전문가',
                'description': 'Kubernetes 클러스터를 프로덕션 환경에서 안정적으로 운영합니다.',
                'objectives': ['클러스터 관리', 'Helm Charts', 'Monitoring', 'Troubleshooting']
            },
            {
                'title': 'Prometheus & Grafana 모니터링',
                'slug': 'prometheus-grafana-monitoring',
                'category': 'cloud',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 129000,
                'short_description': '완벽한 시스템 모니터링',
                'description': 'Prometheus와 Grafana로 시스템을 실시간 모니터링합니다.',
                'objectives': ['메트릭 수집', 'PromQL', '대시보드 구축', 'Alert 설정']
            },
            {
                'title': 'Serverless Architecture 설계',
                'slug': 'serverless-architecture-design',
                'category': 'cloud',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 159000,
                'short_description': '서버리스 아키텍처 완전 정복',
                'description': 'AWS Lambda, API Gateway 등으로 서버리스 애플리케이션을 구축합니다.',
                'objectives': ['Lambda 함수', 'API Gateway', 'DynamoDB', 'SAM/CDK']
            },

            # 게임 개발 (21-25)
            {
                'title': 'Unreal Engine 5 게임 개발',
                'slug': 'unreal-engine-5-game-dev',
                'category': 'game',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 179000,
                'short_description': 'UE5로 AAA급 게임 만들기',
                'description': 'Unreal Engine 5의 최신 기능으로 고품질 게임을 개발합니다.',
                'objectives': ['Blueprint', 'C++ 프로그래밍', 'Nanite/Lumen', '멀티플레이어']
            },
            {
                'title': 'Godot 게임 엔진 마스터',
                'slug': 'godot-game-engine-master',
                'category': 'game',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 119000,
                'short_description': '오픈소스 게임 엔진의 강자',
                'description': 'Godot으로 2D/3D 게임을 빠르게 개발합니다.',
                'objectives': ['GDScript', 'Scene System', 'Physics', '게임 출시']
            },
            {
                'title': '게임 디자인 이론과 실전',
                'slug': 'game-design-theory-practice',
                'category': 'game',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '재미있는 게임을 만드는 법',
                'description': '게임 디자인의 핵심 원리와 레벨 디자인을 학습합니다.',
                'objectives': ['게임 메카닉', '레벨 디자인', '밸런싱', 'UX']
            },
            {
                'title': '모바일 게임 개발 & 수익화',
                'slug': 'mobile-game-monetization',
                'category': 'game',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 139000,
                'short_description': '수익 내는 모바일 게임 만들기',
                'description': 'Unity로 모바일 게임을 개발하고 수익화 전략을 실행합니다.',
                'objectives': ['모바일 최적화', 'IAP', '광고 수익', '게임 마케팅']
            },
            {
                'title': 'VR/AR 게임 개발',
                'slug': 'vr-ar-game-development',
                'category': 'game',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 169000,
                'short_description': '몰입형 게임 경험 창조',
                'description': 'VR/AR 기기를 위한 몰입형 게임을 개발합니다.',
                'objectives': ['XR Toolkit', 'Hand Tracking', 'Spatial Audio', '최적화']
            },

            # 예술 & 창작 (26-30)
            {
                'title': '음악 프로듀싱 with Ableton Live',
                'slug': 'music-production-ableton',
                'category': 'creative',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 129000,
                'short_description': 'EDM부터 힙합까지 음악 제작',
                'description': 'Ableton Live로 전문가 수준의 음악을 프로듀싱합니다.',
                'objectives': ['DAW 마스터', '믹싱/마스터링', 'MIDI 제작', '사운드 디자인']
            },
            {
                'title': 'Premiere Pro 영상 편집 프로',
                'slug': 'premiere-pro-video-editing',
                'category': 'creative',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 119000,
                'short_description': 'YouTube부터 영화까지',
                'description': 'Premiere Pro로 전문가 수준의 영상을 편집합니다.',
                'objectives': ['편집 기법', '컬러 그레이딩', '오디오 믹싱', 'VFX']
            },
            {
                'title': 'DaVinci Resolve 컬러 그레이딩',
                'slug': 'davinci-resolve-color-grading',
                'category': 'creative',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 149000,
                'short_description': '시네마틱 컬러 작업',
                'description': 'DaVinci Resolve로 영화 같은 색감을 연출합니다.',
                'objectives': ['Color Wheels', 'LUT 활용', 'Node 작업', '스킨톤 보정']
            },
            {
                'title': '사진 촬영 & 보정 마스터',
                'slug': 'photography-retouching-master',
                'category': 'creative',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 109000,
                'short_description': '카메라 기초부터 Lightroom까지',
                'description': '사진 촬영 기법과 Lightroom/Photoshop 보정을 마스터합니다.',
                'objectives': ['노출/구도', 'Lightroom', 'Photoshop', '포트폴리오']
            },
            {
                'title': '디지털 드로잉 & 일러스트',
                'slug': 'digital-drawing-illustration',
                'category': 'creative',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 99000,
                'short_description': 'iPad/타블렛으로 그림 그리기',
                'description': 'Procreate와 Clip Studio로 디지털 일러스트를 그립니다.',
                'objectives': ['기초 드로잉', '채색 기법', '캐릭터 디자인', '배경 작업']
            },

            # 금융 & 투자 (31-35)
            {
                'title': '주식 투자 기초부터 실전까지',
                'slug': 'stock-investment-complete',
                'category': 'finance',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 149000,
                'short_description': '성공하는 주식 투자 전략',
                'description': '주식 투자의 기초부터 고급 전략까지 모든 것을 배웁니다.',
                'objectives': ['기본 분석', '기술적 분석', '종목 선정', '리스크 관리']
            },
            {
                'title': '암호화폐 투자 & 트레이딩',
                'slug': 'cryptocurrency-trading',
                'category': 'finance',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 129000,
                'short_description': '비트코인부터 DeFi까지',
                'description': '암호화폐 시장 분석과 안전한 투자 전략을 학습합니다.',
                'objectives': ['블록체인 이해', '거래소 활용', 'DeFi', '포트폴리오']
            },
            {
                'title': '부동산 투자 실전 전략',
                'slug': 'real-estate-investment',
                'category': 'finance',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 159000,
                'short_description': '부동산으로 자산 증식',
                'description': '부동산 투자의 모든 것을 실전 사례로 배웁니다.',
                'objectives': ['입지 분석', '수익률 계산', '세금 전략', '경매/공매']
            },
            {
                'title': '퀀트 트레이딩 with Python',
                'slug': 'quant-trading-python',
                'category': 'finance',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 199000,
                'short_description': '알고리즘 트레이딩 시스템 구축',
                'description': 'Python으로 자동 트레이딩 시스템을 개발합니다.',
                'objectives': ['백테스팅', '전략 개발', 'API 연동', '리스크 관리']
            },
            {
                'title': '재무 제표 분석 & 가치 투자',
                'slug': 'financial-statement-analysis',
                'category': 'finance',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 139000,
                'short_description': '워렌 버핏의 투자 철학',
                'description': '재무제표를 읽고 저평가된 기업을 찾아냅니다.',
                'objectives': ['재무제표 읽기', '가치 평가', 'DCF 모델', '안전 마진']
            },

            # 건강 & 피트니스 (36-40)
            {
                'title': '요가 지도자 양성 과정',
                'slug': 'yoga-instructor-certification',
                'category': 'health',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 199000,
                'short_description': '요가 강사 자격증 준비',
                'description': '전문 요가 강사가 되기 위한 완벽한 과정입니다.',
                'objectives': ['아사나', '호흡법', '명상', '해부학']
            },
            {
                'title': '필라테스 홈 트레이닝',
                'slug': 'pilates-home-training',
                'category': 'health',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '집에서 하는 필라테스',
                'description': '특별한 장비 없이 집에서 필라테스를 즐깁니다.',
                'objectives': ['코어 강화', '자세 교정', '유연성', '통증 완화']
            },
            {
                'title': '근력 운동 완벽 가이드',
                'slug': 'strength-training-complete',
                'category': 'health',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '헬스장 운동 마스터',
                'description': '과학적인 근력 운동으로 건강한 몸을 만듭니다.',
                'objectives': ['운동 루틴', '영양 관리', '회복', '부상 예방']
            },
            {
                'title': '마라톤 완주 트레이닝',
                'slug': 'marathon-training-program',
                'category': 'health',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '0부터 42.195km까지',
                'description': '체계적인 훈련으로 마라톤 풀코스를 완주합니다.',
                'objectives': ['훈련 계획', '페이스 관리', '부상 예방', '멘탈 관리']
            },
            {
                'title': '건강한 식습관 & 다이어트',
                'slug': 'healthy-eating-diet',
                'category': 'health',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 69000,
                'short_description': '지속 가능한 건강 관리',
                'description': '과학적 근거에 기반한 건강한 식습관을 만듭니다.',
                'objectives': ['영양학 기초', '칼로리 계산', '식단 관리', '습관 형성']
            },

            # 취미 & 라이프스타일 (41-45)
            {
                'title': '홈 베이킹 마스터',
                'slug': 'home-baking-master',
                'category': 'lifestyle',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 89000,
                'short_description': '빵부터 케이크까지',
                'description': '집에서 전문가 수준의 베이킹을 즐깁니다.',
                'objectives': ['기본 빵', '케이크', '쿠키', '페이스트리']
            },
            {
                'title': '한식 요리 완벽 가이드',
                'slug': 'korean-cooking-complete',
                'category': 'lifestyle',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '집밥이 최고야',
                'description': '한식의 기본부터 응용까지 요리 실력을 키웁니다.',
                'objectives': ['기본 양념', '국/찌개', '볶음/조림', '특별 요리']
            },
            {
                'title': '바리스타 카페 창업',
                'slug': 'barista-cafe-startup',
                'category': 'lifestyle',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 149000,
                'short_description': '커피 전문가 되기',
                'description': '바리스타 자격증부터 카페 창업까지 모든 과정을 배웁니다.',
                'objectives': ['커피 이론', '에스프레소', '라떼 아트', '창업 실무']
            },
            {
                'title': '가드닝 & 식물 키우기',
                'slug': 'gardening-plant-care',
                'category': 'lifestyle',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 59000,
                'short_description': '초보 식집사를 위한 가이드',
                'description': '식물을 건강하게 키우는 모든 노하우를 배웁니다.',
                'objectives': ['식물 선택', '물 주기', '병해충', '번식']
            },
            {
                'title': '여행 사진 & 영상 촬영',
                'slug': 'travel-photography-videography',
                'category': 'lifestyle',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '여행을 추억으로 남기기',
                'description': '여행지에서 멋진 사진과 영상을 촬영하는 법을 배웁니다.',
                'objectives': ['구도 잡기', '모바일 촬영', '편집', 'SNS 활용']
            },

            # 자기계발 & 비즈니스 (46-50)
            {
                'title': '생산성 & 시간 관리 마스터',
                'slug': 'productivity-time-management',
                'category': 'business',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 79000,
                'short_description': '하루 24시간을 48시간처럼',
                'description': '생산성을 극대화하는 시스템을 구축합니다.',
                'objectives': ['우선순위', 'Notion 활용', '습관 형성', '번아웃 예방']
            },
            {
                'title': '리더십 & 팀 관리',
                'slug': 'leadership-team-management',
                'category': 'business',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 129000,
                'short_description': '존경받는 리더 되기',
                'description': '효과적인 리더십으로 팀을 성공으로 이끕니다.',
                'objectives': ['리더십 스타일', '동기부여', '갈등 해결', '성과 관리']
            },
            {
                'title': '프레젠테이션 & 스피치',
                'slug': 'presentation-public-speaking',
                'category': 'business',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 99000,
                'short_description': '청중을 사로잡는 발표',
                'description': '자신감 있게 청중 앞에서 발표하는 기술을 배웁니다.',
                'objectives': ['구조 설계', '슬라이드', '보디랭귀지', '질의응답']
            },
            {
                'title': '1인 창업 & 사이드 프로젝트',
                'slug': 'solo-entrepreneurship',
                'category': 'business',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 149000,
                'short_description': 'N잡러를 위한 가이드',
                'description': '본업을 유지하며 수익을 창출하는 사이드 프로젝트를 시작합니다.',
                'objectives': ['아이디어 검증', 'MVP 개발', '마케팅', '수익화']
            },
            {
                'title': '협상 & 설득의 심리학',
                'slug': 'negotiation-persuasion-psychology',
                'category': 'business',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 119000,
                'short_description': 'Win-Win 협상 전략',
                'description': '심리학을 활용한 협상과 설득 기술을 마스터합니다.',
                'objectives': ['협상 이론', '설득 기법', '거절 대응', '실전 연습']
            },
        ]

        created_count = 0
        for idx, course_data in enumerate(courses_data):
            if Course.objects.filter(slug=course_data['slug']).exists():
                self.stdout.write(f'  ⏭️  Skipping {course_data["slug"]} (already exists)')
                continue

            # Get random instructor
            instructor = random.choice(instructors)

            # Extract fields
            objectives = course_data.pop('objectives')
            price = course_data.pop('price', 0)

            # Create course
            course = Course.objects.create(
                instructor=instructor,
                price=price,
                is_published=True,
                total_enrollments=random.randint(30, 3000),
                average_rating=round(random.uniform(4.0, 5.0), 1),
                rating_count=random.randint(5, 800),
                total_duration_minutes=random.randint(300, 2400),
                **course_data
            )
            course.learning_objectives = objectives
            course.save()

            # Create basic modules (will be expanded by add_50_modules command)
            module_titles = ['입문', '초급', '중급', '고급', '마스터']
            for mod_idx, mod_title in enumerate(module_titles[:3]):
                module = Module.objects.create(
                    course=course,
                    title=mod_title,
                    description=f'{mod_title} 단계 학습',
                    order=mod_idx
                )

                # Create basic lessons
                for les_idx in range(3):
                    Lesson.objects.create(
                        module=module,
                        title=f'{mod_title} 레슨 {les_idx + 1}',
                        lesson_type='video',
                        content=f'{mod_title} 단계의 학습 내용입니다.',
                        order=les_idx,
                        is_preview=(mod_idx == 0 and les_idx == 0),
                        video_duration=random.randint(600, 1800)
                    )

            # Create practice questions
            for _ in range(random.randint(5, 10)):
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

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully created {created_count} new courses!'
                f'\n📚 Categories:'
                f'\n   - 고급 프로그래밍: 10 courses'
                f'\n   - 클라우드 & DevOps: 10 courses'
                f'\n   - 게임 개발: 5 courses'
                f'\n   - 예술 & 창작: 5 courses'
                f'\n   - 금융 & 투자: 5 courses'
                f'\n   - 건강 & 피트니스: 5 courses'
                f'\n   - 취미 & 라이프스타일: 5 courses'
                f'\n   - 자기계발 & 비즈니스: 5 courses'
            )
        )
