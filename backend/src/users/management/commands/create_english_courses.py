from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User
from courses.models import Course, Module, Lesson
from ai.models import PracticeQuestion
import random


class Command(BaseCommand):
    help = 'Create comprehensive English education courses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating English education courses...')

        # Create instructor if doesn't exist
        instructor, created = User.objects.get_or_create(
            username='english_teacher',
            defaults={
                'email': 'english@example.com',
                'user_type': 'instructor',
                'first_name': 'Sarah',
                'last_name': 'Johnson'
            }
        )
        if created:
            instructor.set_password('instructor123')
            instructor.save()
            self.stdout.write(self.style.SUCCESS(f'Created instructor: {instructor.username}'))

        # Define English courses
        courses_data = [
            # 시험 대비 과정
            {
                'title': 'TOEIC 900+ 완성 과정',
                'slug': 'toeic-900-complete',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 129000,
                'duration_hours': 40,
                'short_description': '토익 900점 이상을 위한 완벽 대비',
                'description': 'TOEIC 시험의 모든 파트를 체계적으로 학습하여 900점 이상을 목표로 합니다. 실전 문제 풀이와 전략을 집중 학습합니다.',
                'objectives': ['LC 만점 전략', 'RC 고득점 비법', '실전 모의고사 10회', '약점 파트 집중 공략'],
                'enrollments': 1850,
                'rating': 4.8,
                'modules': [
                    {
                        'title': 'TOEIC LC Part 1-2 마스터',
                        'order': 1,
                        'lessons': [
                            {'title': 'Part 1 사진 묘사 전략', 'duration': 45, 'type': 'video'},
                            {'title': 'Part 1 필수 어휘 200', 'duration': 30, 'type': 'video'},
                            {'title': 'Part 2 질문 유형 분석', 'duration': 50, 'type': 'video'},
                            {'title': 'Part 2 함정 답안 피하기', 'duration': 40, 'type': 'video'},
                            {'title': 'Part 1-2 실전 문제 100제', 'duration': 60, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': 'TOEIC LC Part 3-4 완성',
                        'order': 2,
                        'lessons': [
                            {'title': 'Part 3 대화 청취 전략', 'duration': 55, 'type': 'video'},
                            {'title': 'Part 3 비즈니스 상황 어휘', 'duration': 35, 'type': 'video'},
                            {'title': 'Part 4 설명문 청취 기법', 'duration': 50, 'type': 'video'},
                            {'title': 'Part 4 주요 화자 유형', 'duration': 40, 'type': 'video'},
                            {'title': 'Part 3-4 실전 훈련', 'duration': 70, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': 'TOEIC RC Part 5-6 문법',
                        'order': 3,
                        'lessons': [
                            {'title': 'Part 5 품사 문제 정복', 'duration': 45, 'type': 'video'},
                            {'title': 'Part 5 동사 시제와 태', 'duration': 50, 'type': 'video'},
                            {'title': 'Part 6 빈칸 완성 전략', 'duration': 40, 'type': 'video'},
                            {'title': 'Part 5-6 실전 문제 200제', 'duration': 80, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': 'TOEIC RC Part 7 독해',
                        'order': 4,
                        'lessons': [
                            {'title': 'Single Passage 스킬', 'duration': 50, 'type': 'video'},
                            {'title': 'Multiple Passage 공략', 'duration': 55, 'type': 'video'},
                            {'title': '빠른 스캐닝 기법', 'duration': 40, 'type': 'video'},
                            {'title': 'Part 7 실전 연습', 'duration': 90, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': '실전 모의고사 & 분석',
                        'order': 5,
                        'lessons': [
                            {'title': '실전 모의고사 1회', 'duration': 120, 'type': 'quiz'},
                            {'title': '실전 모의고사 2회', 'duration': 120, 'type': 'quiz'},
                            {'title': '실전 모의고사 3회', 'duration': 120, 'type': 'quiz'},
                            {'title': '오답 분석 및 보완', 'duration': 60, 'type': 'video'},
                        ]
                    }
                ],
                'practice_questions': [
                    {'question': 'TOEIC Part 1에서 사진을 보고 가장 적절한 설명을 고르는 전략은?', 'correct_answer': '핵심 객체와 동작을 먼저 파악하고, 세부 사항을 확인한다', 'difficulty': 'medium'},
                    {'question': 'TOEIC Part 5 품사 문제에서 빈칸 앞뒤를 보고 판단해야 할 것은?', 'correct_answer': '문장 구조와 의미상 필요한 품사', 'difficulty': 'medium'},
                    {'question': 'TOEIC Part 7 Multiple Passage에서 효율적인 접근법은?', 'correct_answer': '질문을 먼저 읽고, 관련 지문을 찾아 읽는다', 'difficulty': 'hard'},
                    {'question': 'TOEIC LC에서 함정 답안을 피하는 방법은?', 'correct_answer': '지문에 나온 단어만으로 답을 선택하지 않고, 의미를 파악한다', 'difficulty': 'medium'},
                    {'question': 'TOEIC 시험에서 시간 관리의 핵심은?', 'correct_answer': 'Part 5-6을 20분 내에 끝내고 Part 7에 충분한 시간 확보', 'difficulty': 'easy'},
                ]
            },
            {
                'title': 'TOEFL iBT 100+ 달성',
                'slug': 'toefl-ibt-100',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 159000,
                'duration_hours': 50,
                'short_description': '토플 100점 이상 목표 완성 과정',
                'description': 'TOEFL iBT Reading, Listening, Speaking, Writing 4개 영역을 모두 마스터하여 100점 이상을 달성합니다.',
                'objectives': ['Reading 25+', 'Listening 25+', 'Speaking 23+', 'Writing 25+'],
                'enrollments': 980,
                'rating': 4.9,
                'modules': [
                    {
                        'title': 'TOEFL Reading 전략',
                        'order': 1,
                        'lessons': [
                            {'title': 'Academic 지문 읽기 전략', 'duration': 50, 'type': 'video'},
                            {'title': 'Vocabulary Questions 공략', 'duration': 40, 'type': 'video'},
                            {'title': 'Inference Questions 마스터', 'duration': 45, 'type': 'video'},
                            {'title': 'Summary Questions 완성', 'duration': 45, 'type': 'video'},
                            {'title': 'Reading 실전 연습', 'duration': 80, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': 'TOEFL Listening 완성',
                        'order': 2,
                        'lessons': [
                            {'title': 'Conversation 청취 기법', 'duration': 45, 'type': 'video'},
                            {'title': 'Lecture 노트테이킹', 'duration': 50, 'type': 'video'},
                            {'title': 'Main Idea 파악하기', 'duration': 40, 'type': 'video'},
                            {'title': 'Detail Questions 대응', 'duration': 40, 'type': 'video'},
                            {'title': 'Listening 실전 훈련', 'duration': 70, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': 'TOEFL Speaking 고득점',
                        'order': 3,
                        'lessons': [
                            {'title': 'Independent Task 전략', 'duration': 50, 'type': 'video'},
                            {'title': 'Integrated Task 준비', 'duration': 55, 'type': 'video'},
                            {'title': '명확한 발음과 억양', 'duration': 40, 'type': 'video'},
                            {'title': '템플릿 활용법', 'duration': 35, 'type': 'video'},
                            {'title': 'Speaking 실전 연습', 'duration': 60, 'type': 'assignment'},
                        ]
                    },
                    {
                        'title': 'TOEFL Writing 마스터',
                        'order': 4,
                        'lessons': [
                            {'title': 'Integrated Writing 구조', 'duration': 45, 'type': 'video'},
                            {'title': 'Independent Writing 전개', 'duration': 50, 'type': 'video'},
                            {'title': '고급 어휘와 표현', 'duration': 40, 'type': 'video'},
                            {'title': '에세이 샘플 분석', 'duration': 45, 'type': 'video'},
                            {'title': 'Writing 첨삭 피드백', 'duration': 70, 'type': 'assignment'},
                        ]
                    },
                ],
                'practice_questions': [
                    {'question': 'TOEFL Reading에서 Inference Question을 풀 때 주의할 점은?', 'correct_answer': '지문에 명시되지 않았지만 논리적으로 추론 가능한 답을 선택한다', 'difficulty': 'hard'},
                    {'question': 'TOEFL Listening Lecture에서 효과적인 노트테이킹 방법은?', 'correct_answer': '주요 아이디어와 예시를 구분하여 간략하게 기록한다', 'difficulty': 'medium'},
                    {'question': 'TOEFL Speaking Independent Task의 준비 시간은?', 'correct_answer': '15초', 'difficulty': 'easy'},
                    {'question': 'TOEFL Integrated Writing의 권장 단어 수는?', 'correct_answer': '150-225 words', 'difficulty': 'easy'},
                ]
            },
            {
                'title': 'IELTS 7.0+ 완벽 대비',
                'slug': 'ielts-7-complete',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 149000,
                'duration_hours': 45,
                'short_description': 'IELTS 7.0 이상 목표 전략',
                'description': 'IELTS Academic 모듈의 4개 영역을 체계적으로 학습하여 Overall 7.0 이상을 달성합니다.',
                'objectives': ['Reading 7.0+', 'Listening 7.0+', 'Speaking 7.0+', 'Writing 6.5+'],
                'enrollments': 750,
                'rating': 4.8,
                'modules': [
                    {
                        'title': 'IELTS Reading 전략',
                        'order': 1,
                        'lessons': [
                            {'title': 'True/False/Not Given 마스터', 'duration': 50, 'type': 'video'},
                            {'title': 'Matching Headings 기법', 'duration': 45, 'type': 'video'},
                            {'title': 'Summary Completion 전략', 'duration': 40, 'type': 'video'},
                            {'title': 'Reading 실전 연습', 'duration': 60, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': 'IELTS Writing Task 1 & 2',
                        'order': 2,
                        'lessons': [
                            {'title': 'Task 1 그래프 분석', 'duration': 50, 'type': 'video'},
                            {'title': 'Task 2 에세이 구조', 'duration': 55, 'type': 'video'},
                            {'title': 'Band 7+ 어휘와 표현', 'duration': 45, 'type': 'video'},
                            {'title': 'Writing 실전 및 첨삭', 'duration': 80, 'type': 'assignment'},
                        ]
                    },
                    {
                        'title': 'IELTS Speaking Part 1-3',
                        'order': 3,
                        'lessons': [
                            {'title': 'Part 1 자기소개와 일상', 'duration': 40, 'type': 'video'},
                            {'title': 'Part 2 Long Turn 준비', 'duration': 50, 'type': 'video'},
                            {'title': 'Part 3 토론 스킬', 'duration': 45, 'type': 'video'},
                            {'title': 'Speaking 모의 테스트', 'duration': 60, 'type': 'assignment'},
                        ]
                    },
                ],
                'practice_questions': [
                    {'question': 'IELTS Reading에서 True/False/Not Given 문제의 핵심은?', 'correct_answer': '지문에 정보가 있는지, 반대인지, 언급 없는지를 정확히 구분한다', 'difficulty': 'medium'},
                    {'question': 'IELTS Writing Task 1의 권장 단어 수는?', 'correct_answer': '최소 150 words', 'difficulty': 'easy'},
                    {'question': 'IELTS Speaking Part 2에서 말해야 하는 시간은?', 'correct_answer': '1-2분', 'difficulty': 'easy'},
                ]
            },

            # 실용 영어 과정
            {
                'title': '영문법 완벽 마스터',
                'slug': 'english-grammar-master',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 69000,
                'duration_hours': 30,
                'short_description': '기초부터 고급까지 영문법 총정리',
                'description': '영어 문법의 모든 것을 체계적으로 학습합니다. 기초 문법부터 고급 구문까지 완벽하게 마스터합니다.',
                'objectives': ['12시제 완벽 이해', '조동사와 가정법', '관계사와 접속사', '분사와 부정사'],
                'enrollments': 2340,
                'rating': 4.7,
                'modules': [
                    {
                        'title': '기초 문법 다지기',
                        'order': 1,
                        'lessons': [
                            {'title': '8품사 완벽 정리', 'duration': 40, 'type': 'video'},
                            {'title': '문장의 5형식', 'duration': 45, 'type': 'video'},
                            {'title': '현재/과거/미래 시제', 'duration': 40, 'type': 'video'},
                            {'title': '기초 문법 테스트', 'duration': 30, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': '중급 문법 완성',
                        'order': 2,
                        'lessons': [
                            {'title': '완료 시제 마스터', 'duration': 50, 'type': 'video'},
                            {'title': '수동태 완벽 이해', 'duration': 40, 'type': 'video'},
                            {'title': '조동사 총정리', 'duration': 45, 'type': 'video'},
                            {'title': '부정사와 동명사', 'duration': 50, 'type': 'video'},
                            {'title': '중급 문법 테스트', 'duration': 40, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': '고급 문법 마스터',
                        'order': 3,
                        'lessons': [
                            {'title': '가정법 완벽 정복', 'duration': 55, 'type': 'video'},
                            {'title': '관계대명사/관계부사', 'duration': 50, 'type': 'video'},
                            {'title': '분사구문 마스터', 'duration': 45, 'type': 'video'},
                            {'title': '접속사와 전치사', 'duration': 40, 'type': 'video'},
                            {'title': '고급 문법 종합 테스트', 'duration': 50, 'type': 'quiz'},
                        ]
                    },
                ],
                'practice_questions': [
                    {'question': '현재완료 시제는 언제 사용하나요?', 'correct_answer': '과거에 시작되어 현재까지 영향을 미치거나 계속되는 상황', 'difficulty': 'easy'},
                    {'question': '가정법 과거완료는 어떤 상황을 나타내나요?', 'correct_answer': '과거 사실의 반대 가정', 'difficulty': 'medium'},
                    {'question': '관계대명사 that과 which의 차이는?', 'correct_answer': 'that은 제한적 용법, which는 계속적 용법 가능', 'difficulty': 'medium'},
                    {'question': '분사구문을 만들 때 주의할 점은?', 'correct_answer': '주절과 종속절의 주어가 같아야 한다', 'difficulty': 'hard'},
                ]
            },
            {
                'title': '영어 작문 실력 향상',
                'slug': 'english-writing-skills',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 89000,
                'duration_hours': 25,
                'short_description': '논리적이고 설득력 있는 영어 글쓰기',
                'description': '다양한 주제의 영어 작문을 체계적으로 학습합니다. 에세이, 이메일, 리포트 작성법을 마스터합니다.',
                'objectives': ['에세이 구조 마스터', '논리적 전개', '고급 어휘 활용', '피드백 반영'],
                'enrollments': 890,
                'rating': 4.6,
                'modules': [
                    {
                        'title': '작문 기초 다지기',
                        'order': 1,
                        'lessons': [
                            {'title': '문장 구조 완성하기', 'duration': 40, 'type': 'video'},
                            {'title': '패러그래프 작성법', 'duration': 45, 'type': 'video'},
                            {'title': '주제문과 뒷받침문', 'duration': 40, 'type': 'video'},
                            {'title': '기초 작문 연습', 'duration': 50, 'type': 'assignment'},
                        ]
                    },
                    {
                        'title': 'Academic Writing',
                        'order': 2,
                        'lessons': [
                            {'title': '에세이 구조 (서론-본론-결론)', 'duration': 50, 'type': 'video'},
                            {'title': '논증 에세이 작성', 'duration': 55, 'type': 'video'},
                            {'title': '인용과 참고문헌', 'duration': 40, 'type': 'video'},
                            {'title': '에세이 첨삭 피드백', 'duration': 70, 'type': 'assignment'},
                        ]
                    },
                    {
                        'title': '실무 영어 작문',
                        'order': 3,
                        'lessons': [
                            {'title': '비즈니스 이메일 작성', 'duration': 45, 'type': 'video'},
                            {'title': '보고서와 제안서', 'duration': 50, 'type': 'video'},
                            {'title': '프레젠테이션 스크립트', 'duration': 40, 'type': 'video'},
                            {'title': '실무 작문 프로젝트', 'duration': 60, 'type': 'assignment'},
                        ]
                    },
                ],
                'practice_questions': [
                    {'question': '효과적인 에세이 서론에 포함되어야 할 것은?', 'correct_answer': '배경 정보, 논제, 주장(thesis statement)', 'difficulty': 'medium'},
                    {'question': '비즈니스 이메일에서 피해야 할 표현은?', 'correct_answer': '너무 캐주얼하거나 감정적인 표현', 'difficulty': 'easy'},
                    {'question': '논증 에세이의 본론 구조는?', 'correct_answer': '주제문 - 근거 - 예시 - 설명', 'difficulty': 'medium'},
                ]
            },
            {
                'title': '영어 발음 교정 완벽 가이드',
                'slug': 'english-pronunciation-perfect',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 59000,
                'duration_hours': 20,
                'short_description': '원어민 같은 발음 만들기',
                'description': '영어 발음의 기초부터 고급까지 체계적으로 교정합니다. 개별 음소, 억양, 리듬을 마스터합니다.',
                'objectives': ['자음/모음 정확한 발음', '연음 규칙', '강세와 억양', '쉐도잉 훈련'],
                'enrollments': 1560,
                'rating': 4.7,
                'modules': [
                    {
                        'title': '기본 발음 마스터',
                        'order': 1,
                        'lessons': [
                            {'title': '영어 자음 완벽 정리', 'duration': 40, 'type': 'video'},
                            {'title': '영어 모음 소리 구분', 'duration': 45, 'type': 'video'},
                            {'title': '한국인이 어려워하는 발음', 'duration': 40, 'type': 'video'},
                            {'title': '발음 연습 1', 'duration': 30, 'type': 'assignment'},
                        ]
                    },
                    {
                        'title': '연음과 리듬',
                        'order': 2,
                        'lessons': [
                            {'title': '연음 규칙 총정리', 'duration': 45, 'type': 'video'},
                            {'title': '강세와 약세', 'duration': 40, 'type': 'video'},
                            {'title': '문장 리듬 익히기', 'duration': 40, 'type': 'video'},
                            {'title': '리듬 연습', 'duration': 35, 'type': 'assignment'},
                        ]
                    },
                    {
                        'title': '억양과 실전 연습',
                        'order': 3,
                        'lessons': [
                            {'title': '억양 패턴 마스터', 'duration': 45, 'type': 'video'},
                            {'title': '쉐도잉 기법', 'duration': 40, 'type': 'video'},
                            {'title': '실전 대화 연습', 'duration': 50, 'type': 'video'},
                            {'title': '발음 종합 평가', 'duration': 40, 'type': 'assignment'},
                        ]
                    },
                ],
                'practice_questions': [
                    {'question': 'th 발음을 정확히 하는 방법은?', 'correct_answer': '혀를 윗니와 아랫니 사이에 살짝 내밀고 발음한다', 'difficulty': 'easy'},
                    {'question': '연음이 일어나는 경우는?', 'correct_answer': '자음으로 끝나는 단어 뒤에 모음으로 시작하는 단어가 올 때', 'difficulty': 'medium'},
                    {'question': '영어의 강세와 약세가 중요한 이유는?', 'correct_answer': '영어는 강세 박자 언어로, 리듬이 의미 전달에 중요하다', 'difficulty': 'medium'},
                ]
            },
            {
                'title': '영어 청취 집중 트레이닝',
                'slug': 'english-listening-intensive',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 79000,
                'duration_hours': 35,
                'short_description': '원어민 영어 100% 이해하기',
                'description': '다양한 액센트와 상황의 영어를 청취하고 이해하는 능력을 향상시킵니다. 뉴스, 팟캐스트, 영화 등을 활용합니다.',
                'objectives': ['다양한 액센트 이해', '빠른 속도 청취', '실생활 영어', '받아쓰기 훈련'],
                'enrollments': 1230,
                'rating': 4.6,
                'modules': [
                    {
                        'title': '기초 청취 훈련',
                        'order': 1,
                        'lessons': [
                            {'title': '청취 전략과 기법', 'duration': 40, 'type': 'video'},
                            {'title': '일상 대화 청취', 'duration': 45, 'type': 'video'},
                            {'title': '핵심 내용 파악하기', 'duration': 40, 'type': 'video'},
                            {'title': '청취 연습 1단계', 'duration': 50, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': '중급 청취 - 다양한 주제',
                        'order': 2,
                        'lessons': [
                            {'title': 'BBC 뉴스 청취', 'duration': 50, 'type': 'video'},
                            {'title': 'TED Talks 이해하기', 'duration': 55, 'type': 'video'},
                            {'title': '팟캐스트 청취 훈련', 'duration': 45, 'type': 'video'},
                            {'title': '받아쓰기 연습', 'duration': 60, 'type': 'assignment'},
                        ]
                    },
                    {
                        'title': '고급 청취 - 실전 영어',
                        'order': 3,
                        'lessons': [
                            {'title': '영화와 드라마 청취', 'duration': 60, 'type': 'video'},
                            {'title': '다양한 액센트 (미국/영국/호주)', 'duration': 50, 'type': 'video'},
                            {'title': '빠른 속도 영어 청취', 'duration': 45, 'type': 'video'},
                            {'title': '종합 청취 테스트', 'duration': 70, 'type': 'quiz'},
                        ]
                    },
                ],
                'practice_questions': [
                    {'question': '효과적인 영어 청취 전략은?', 'correct_answer': '모든 단어를 들으려 하지 말고 핵심 내용을 파악한다', 'difficulty': 'easy'},
                    {'question': '받아쓰기(dictation)의 효과는?', 'correct_answer': '정확한 청취력과 철자 능력을 동시에 향상시킨다', 'difficulty': 'medium'},
                    {'question': '빠른 영어를 이해하기 위한 방법은?', 'correct_answer': '연음 규칙을 이해하고 반복 청취 연습을 한다', 'difficulty': 'medium'},
                ]
            },
            {
                'title': '미드로 배우는 실전 영어',
                'slug': 'english-with-tv-shows',
                'category': 'language',
                'difficulty': 'intermediate',
                'price_type': 'paid',
                'price': 69000,
                'duration_hours': 30,
                'short_description': '인기 미드로 재미있게 배우는 영어',
                'description': '인기 미국 드라마를 활용하여 실생활 영어 표현과 문화를 자연스럽게 학습합니다.',
                'objectives': ['실생활 영어 표현', '슬랭과 관용어', '미국 문화 이해', '쉐도잉 연습'],
                'enrollments': 1820,
                'rating': 4.8,
                'modules': [
                    {
                        'title': 'Friends로 배우는 일상 영어',
                        'order': 1,
                        'lessons': [
                            {'title': '일상 대화 표현 20', 'duration': 45, 'type': 'video'},
                            {'title': '유머와 농담 이해하기', 'duration': 40, 'type': 'video'},
                            {'title': 'Friends 주요 장면 분석', 'duration': 50, 'type': 'video'},
                            {'title': '대화 연습', 'duration': 35, 'type': 'assignment'},
                        ]
                    },
                    {
                        'title': 'The Office로 배우는 비즈니스 영어',
                        'order': 2,
                        'lessons': [
                            {'title': '직장 영어 표현', 'duration': 45, 'type': 'video'},
                            {'title': '회의와 프레젠테이션', 'duration': 40, 'type': 'video'},
                            {'title': '이메일 영어', 'duration': 35, 'type': 'video'},
                            {'title': '역할극 연습', 'duration': 40, 'type': 'assignment'},
                        ]
                    },
                    {
                        'title': 'Modern Family로 배우는 가족 영어',
                        'order': 3,
                        'lessons': [
                            {'title': '가족 간 대화', 'duration': 40, 'type': 'video'},
                            {'title': '감정 표현하기', 'duration': 35, 'type': 'video'},
                            {'title': '슬랭과 축약어', 'duration': 40, 'type': 'video'},
                            {'title': '종합 리뷰', 'duration': 45, 'type': 'video'},
                        ]
                    },
                ],
                'practice_questions': [
                    {'question': '"I\'m gonna"는 무슨 뜻인가요?', 'correct_answer': 'I am going to의 축약형', 'difficulty': 'easy'},
                    {'question': '"Hang out"의 의미는?', 'correct_answer': '친구들과 시간을 보내다', 'difficulty': 'easy'},
                    {'question': '미드로 영어를 공부할 때 효과적인 방법은?', 'correct_answer': '자막 없이 보기 → 한글 자막 → 영어 자막 순으로 반복', 'difficulty': 'medium'},
                ]
            },
            {
                'title': '여행 영어 완벽 가이드',
                'slug': 'travel-english-complete',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'free',
                'short_description': '해외여행 필수 영어 표현',
                'description': '공항, 호텔, 레스토랑, 쇼핑 등 여행 상황별 필수 영어 표현을 학습합니다.',
                'objectives': ['공항 영어', '호텔 체크인/아웃', '레스토랑 주문', '쇼핑 영어'],
                'enrollments': 3240,
                'rating': 4.5,
                'duration_hours': 15,
                'modules': [
                    {
                        'title': '공항과 비행기',
                        'order': 1,
                        'lessons': [
                            {'title': '체크인과 보딩', 'duration': 30, 'type': 'video'},
                            {'title': '기내 서비스 영어', 'duration': 25, 'type': 'video'},
                            {'title': '입국 심사', 'duration': 30, 'type': 'video'},
                            {'title': '공항 영어 연습', 'duration': 20, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': '숙박 영어',
                        'order': 2,
                        'lessons': [
                            {'title': '호텔 예약과 체크인', 'duration': 30, 'type': 'video'},
                            {'title': '룸서비스와 컴플레인', 'duration': 25, 'type': 'video'},
                            {'title': '체크아웃', 'duration': 20, 'type': 'video'},
                            {'title': '숙박 영어 실습', 'duration': 25, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': '식사와 쇼핑',
                        'order': 3,
                        'lessons': [
                            {'title': '레스토랑 예약과 주문', 'duration': 35, 'type': 'video'},
                            {'title': '쇼핑 영어 표현', 'duration': 30, 'type': 'video'},
                            {'title': '길 찾기', 'duration': 25, 'type': 'video'},
                            {'title': '여행 영어 종합', 'duration': 30, 'type': 'quiz'},
                        ]
                    },
                ],
                'practice_questions': [
                    {'question': '호텔 체크인 시 필요한 표현은?', 'correct_answer': 'I have a reservation under [name]', 'difficulty': 'easy'},
                    {'question': '레스토랑에서 주문할 때 쓰는 표현은?', 'correct_answer': 'I\'ll have / I\'d like to order', 'difficulty': 'easy'},
                    {'question': '길을 물어볼 때 쓰는 표현은?', 'correct_answer': 'Could you tell me how to get to...?', 'difficulty': 'easy'},
                ]
            },
            {
                'title': '어린이 영어 파닉스부터 회화까지',
                'slug': 'kids-english-phonics-conversation',
                'category': 'language',
                'difficulty': 'beginner',
                'price_type': 'paid',
                'price': 99000,
                'duration_hours': 40,
                'short_description': '7-12세 어린이를 위한 영어',
                'description': '파닉스 기초부터 기본 회화까지, 어린이가 재미있게 배울 수 있는 영어 과정입니다.',
                'objectives': ['파닉스 완성', '기초 단어 500개', '기본 회화', '노래와 게임'],
                'enrollments': 1950,
                'rating': 4.9,
                'modules': [
                    {
                        'title': '파닉스 기초',
                        'order': 1,
                        'lessons': [
                            {'title': 'A-Z 알파벳 소리', 'duration': 35, 'type': 'video'},
                            {'title': '단모음 파닉스', 'duration': 40, 'type': 'video'},
                            {'title': '장모음 파닉스', 'duration': 40, 'type': 'video'},
                            {'title': '파닉스 게임', 'duration': 30, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': '기초 단어와 문장',
                        'order': 2,
                        'lessons': [
                            {'title': '색깔과 숫자', 'duration': 30, 'type': 'video'},
                            {'title': '동물과 과일', 'duration': 35, 'type': 'video'},
                            {'title': '가족과 신체', 'duration': 30, 'type': 'video'},
                            {'title': '간단한 문장 만들기', 'duration': 40, 'type': 'video'},
                            {'title': '단어 퀴즈', 'duration': 25, 'type': 'quiz'},
                        ]
                    },
                    {
                        'title': '기본 회화',
                        'order': 3,
                        'lessons': [
                            {'title': '인사와 자기소개', 'duration': 30, 'type': 'video'},
                            {'title': '좋아하는 것 말하기', 'duration': 35, 'type': 'video'},
                            {'title': '날씨와 감정 표현', 'duration': 30, 'type': 'video'},
                            {'title': '노래로 배우는 영어', 'duration': 40, 'type': 'video'},
                        ]
                    },
                ],
                'practice_questions': [
                    {'question': '파닉스란 무엇인가요?', 'correct_answer': '영어 철자와 소리의 관계를 배우는 학습법', 'difficulty': 'easy'},
                    {'question': '"What\'s your name?"에 대한 대답은?', 'correct_answer': 'My name is [이름]', 'difficulty': 'easy'},
                    {'question': '"I like apples"는 무슨 뜻인가요?', 'correct_answer': '나는 사과를 좋아해요', 'difficulty': 'easy'},
                ]
            },
            {
                'title': 'CNN 뉴스 영어 마스터',
                'slug': 'cnn-news-english',
                'category': 'language',
                'difficulty': 'advanced',
                'price_type': 'paid',
                'price': 89000,
                'duration_hours': 28,
                'short_description': 'CNN으로 배우는 고급 영어',
                'description': 'CNN 뉴스를 통해 시사 영어와 고급 어휘를 학습합니다. 정치, 경제, 사회, 과학 등 다양한 주제를 다룹니다.',
                'objectives': ['뉴스 영어 이해', '고급 어휘 1000+', '빠른 청취', '토론 능력'],
                'enrollments': 670,
                'rating': 4.7,
                'modules': [
                    {
                        'title': '뉴스 영어 기초',
                        'order': 1,
                        'lessons': [
                            {'title': '뉴스 구조 이해하기', 'duration': 40, 'type': 'video'},
                            {'title': '정치 뉴스 필수 어휘', 'duration': 45, 'type': 'video'},
                            {'title': '경제 뉴스 용어', 'duration': 45, 'type': 'video'},
                            {'title': '뉴스 요약 연습', 'duration': 50, 'type': 'assignment'},
                        ]
                    },
                    {
                        'title': '심화 뉴스 분석',
                        'order': 2,
                        'lessons': [
                            {'title': '국제 관계 뉴스', 'duration': 50, 'type': 'video'},
                            {'title': '과학 기술 뉴스', 'duration': 45, 'type': 'video'},
                            {'title': '환경과 기후 이슈', 'duration': 40, 'type': 'video'},
                            {'title': '뉴스 토론', 'duration': 60, 'type': 'assignment'},
                        ]
                    },
                ],
                'practice_questions': [
                    {'question': '뉴스 영어의 특징은?', 'correct_answer': '간결하고 객관적이며 고급 어휘를 사용한다', 'difficulty': 'medium'},
                    {'question': '"GDP"는 무엇의 약자인가요?', 'correct_answer': 'Gross Domestic Product (국내총생산)', 'difficulty': 'easy'},
                    {'question': '뉴스를 효과적으로 이해하는 방법은?', 'correct_answer': '배경 지식을 쌓고, 핵심 내용을 파악하며, 반복 청취한다', 'difficulty': 'medium'},
                ]
            },
        ]

        # Create courses
        created_count = 0
        for course_data in courses_data:
            # Extract modules and questions
            modules_data = course_data.pop('modules', [])
            questions_data = course_data.pop('practice_questions', [])
            enrollments = course_data.pop('enrollments', 0)
            rating = course_data.pop('rating', 4.5)
            duration = course_data.pop('duration_hours', 10)

            # Create or update course
            course, created = Course.objects.update_or_create(
                slug=course_data['slug'],
                defaults={
                    **course_data,
                    'instructor': instructor,
                    'is_published': True,
                    'enrollment_count': enrollments,
                    'average_rating': rating,
                    'estimated_duration': duration,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'Created course: {course.title}')

            # Create modules and lessons
            for module_data in modules_data:
                lessons_data = module_data.pop('lessons', [])

                module, _ = Module.objects.update_or_create(
                    course=course,
                    title=module_data['title'],
                    defaults={'order': module_data['order']}
                )

                for idx, lesson_data in enumerate(lessons_data, 1):
                    Lesson.objects.update_or_create(
                        module=module,
                        title=lesson_data['title'],
                        defaults={
                            'order': idx,
                            'content_type': lesson_data.get('type', 'video'),
                            'duration_minutes': lesson_data.get('duration', 30),
                            'is_free_preview': idx == 1,  # First lesson is free
                        }
                    )

            # Create practice questions
            for q_data in questions_data:
                PracticeQuestion.objects.update_or_create(
                    course=course,
                    question=q_data['question'],
                    defaults={
                        'correct_answer': q_data['correct_answer'],
                        'difficulty': q_data.get('difficulty', 'medium'),
                        'explanation': f"정답: {q_data['correct_answer']}"
                    }
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully created {created_count} English courses!'
                f'\n📚 Total: {len(courses_data)} courses'
                f'\n👨‍🏫 Instructor: {instructor.username}'
                f'\n\n🎯 Course Categories:'
                f'\n   - TOEIC, TOEFL, IELTS (Test Prep)'
                f'\n   - Grammar, Writing, Pronunciation'
                f'\n   - Listening, TV Shows, Travel English'
                f'\n   - Kids English, CNN News English'
            )
        )
