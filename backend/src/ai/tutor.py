"""
AI Tutor implementation using Claude API
"""
from anthropic import Anthropic
from django.conf import settings
from typing import List, Dict, Optional
import json


class AITutor:
    """AI Tutor powered by Claude"""

    def __init__(self, course_context: str = "", student_profile: Dict = None):
        self.anthropic = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.course_context = course_context
        self.student_profile = student_profile or {}
        self.conversation_history = []

    async def answer_question(
        self,
        question: str,
        lesson_context: str = "",
        conversation_history: List[Dict] = None
    ) -> Dict:
        """
        Answer student's question with personalized response

        Args:
            question: Student's question
            lesson_context: Context about current lesson
            conversation_history: Previous conversation messages

        Returns:
            Dict with answer and metadata
        """
        system_prompt = self._build_system_prompt(lesson_context)

        messages = conversation_history or []
        messages.append({
            "role": "user",
            "content": question
        })

        try:
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                system=system_prompt,
                messages=messages
            )

            answer = response.content[0].text

            return {
                'answer': answer,
                'tokens_used': response.usage.total_tokens,
                'model': response.model,
                'success': True
            }

        except Exception as e:
            return {
                'answer': f"죄송합니다. 오류가 발생했습니다: {str(e)}",
                'tokens_used': 0,
                'model': '',
                'success': False,
                'error': str(e)
            }

    def _build_system_prompt(self, lesson_context: str) -> str:
        """Build system prompt for Claude"""

        level = self.student_profile.get('learning_level', '초급')
        learning_style = self.student_profile.get('learning_style', 'visual')
        weak_areas = self.student_profile.get('weak_areas', [])
        performance = self.student_profile.get('performance', {})

        prompt = f"""당신은 전문 교육자이자 AI 튜터입니다.

코스 정보:
{self.course_context}

현재 레슨:
{lesson_context}

학생 프로필:
- 학습 수준: {level}
- 학습 스타일: {learning_style}
- 이전 성과: {performance}
- 어려워하는 부분: {', '.join(weak_areas) if weak_areas else '없음'}

튜터링 지침:
1. 학생의 수준에 맞게 설명을 조절하세요
2. 구체적이고 실용적인 예시를 사용하세요
3. 이해를 확인하는 질문을 하세요
4. 격려하고 긍정적인 피드백을 제공하세요
5. 관련 추가 학습 자료를 제안하세요
6. 필요시 단계별로 설명하세요
7. 실습 문제를 제시하여 이해도를 높이세요

응답 형식:
- 명확하고 이해하기 쉬운 한국어로 작성
- 코드 예제는 마크다운 코드 블록 사용
- 복잡한 개념은 비유나 그림으로 설명

항상 학생의 성장을 돕는 것이 목표임을 기억하세요."""

        return prompt

    async def generate_practice_questions(
        self,
        topic: str,
        difficulty: str,
        count: int = 5,
        question_type: str = "multiple_choice"
    ) -> List[Dict]:
        """
        Generate practice questions for a topic

        Args:
            topic: Topic to generate questions for
            difficulty: easy, medium, hard
            count: Number of questions to generate
            question_type: Type of questions (multiple_choice, short_answer, coding)

        Returns:
            List of generated questions
        """
        prompt = f"""다음 주제에 대한 {difficulty} 난이도의 {question_type} 연습 문제를 {count}개 생성해주세요:

주제: {topic}
코스 컨텍스트: {self.course_context}

각 문제는 다음 JSON 형식으로 작성해주세요:
{{
    "question": "문제 내용",
    "options": ["선택지1", "선택지2", "선택지3", "선택지4"],  # multiple_choice인 경우
    "correct_answer": "정답",
    "explanation": "정답 설명 및 해설"
}}

{count}개의 문제를 JSON 배열로 반환해주세요."""

        try:
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse JSON response
            content = response.content[0].text
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            questions = json.loads(content)
            return questions

        except Exception as e:
            print(f"Error generating questions: {e}")
            return []

    async def evaluate_answer(
        self,
        question: str,
        student_answer: str,
        correct_answer: str,
        evaluation_criteria: Dict = None
    ) -> Dict:
        """
        Evaluate student's answer and provide feedback

        Args:
            question: The question asked
            student_answer: Student's answer
            correct_answer: Correct answer
            evaluation_criteria: Criteria for evaluation

        Returns:
            Dict with evaluation results and feedback
        """
        criteria = evaluation_criteria or {
            'correctness': 0.6,
            'explanation': 0.2,
            'clarity': 0.2
        }

        prompt = f"""다음 학생의 답변을 평가해주세요:

질문: {question}

정답: {correct_answer}

학생 답변: {student_answer}

평가 기준:
{json.dumps(criteria, indent=2, ensure_ascii=False)}

다음 JSON 형식으로 평가 결과를 제공해주세요:
{{
    "is_correct": true/false,
    "score": 0-100,
    "feedback": "구체적인 피드백",
    "strengths": ["잘한 점들"],
    "improvements": ["개선할 점들"],
    "suggestions": ["추가 학습 제안"]
}}"""

        try:
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            content = response.content[0].text
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            evaluation = json.loads(content)
            return evaluation

        except Exception as e:
            return {
                'is_correct': False,
                'score': 0,
                'feedback': f"평가 중 오류가 발생했습니다: {str(e)}",
                'strengths': [],
                'improvements': [],
                'suggestions': []
            }

    async def suggest_learning_path(
        self,
        completed_topics: List[str],
        weak_areas: List[str],
        goals: List[str]
    ) -> Dict:
        """
        Suggest personalized learning path based on student's progress

        Args:
            completed_topics: Topics student has completed
            weak_areas: Areas where student struggles
            goals: Student's learning goals

        Returns:
            Dict with suggested learning path
        """
        prompt = f"""학생의 학습 경로를 제안해주세요:

완료한 주제:
{', '.join(completed_topics)}

어려워하는 부분:
{', '.join(weak_areas)}

학습 목표:
{', '.join(goals)}

코스 컨텍스트:
{self.course_context}

다음 JSON 형식으로 학습 경로를 제안해주세요:
{{
    "next_topics": ["다음에 학습할 주제들"],
    "remedial_topics": ["복습이 필요한 주제들"],
    "estimated_time": "예상 소요 시간",
    "priority_order": ["우선순위별 학습 순서"],
    "resources": ["추천 학습 자료"],
    "milestones": ["학습 마일스톤"]
}}"""

        try:
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            content = response.content[0].text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            learning_path = json.loads(content)
            return learning_path

        except Exception as e:
            return {
                'next_topics': [],
                'remedial_topics': weak_areas,
                'estimated_time': 'N/A',
                'priority_order': [],
                'resources': [],
                'milestones': [],
                'error': str(e)
            }
