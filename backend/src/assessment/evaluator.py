"""
Auto-evaluation system using AI
"""
from anthropic import Anthropic
from django.conf import settings
import json


class AutoEvaluator:
    """Automated assignment evaluator"""

    def __init__(self):
        self.anthropic = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def evaluate_code(self, code: str, test_cases: list, rubric: dict) -> dict:
        """Evaluate code assignment"""
        # This would include running tests and AI code review
        return {
            'score': 0,
            'test_results': [],
            'feedback': [],
            'suggestions': []
        }

    async def evaluate_essay(self, essay: str, rubric: dict, reference: str = None) -> dict:
        """Evaluate essay/written assignment"""

        prompt = f"""다음 에세이를 평가해주세요:

에세이 내용:
{essay}

평가 기준:
{json.dumps(rubric, indent=2, ensure_ascii=False)}

다음 JSON 형식으로 평가 결과를 제공해주세요:
{{
    "score": 0-100,
    "feedback": "전체 피드백",
    "strengths": ["강점들"],
    "weaknesses": ["약점들"],
    "suggestions": ["개선 제안"],
    "rubric_scores": {{"기준1": 점수, "기준2": 점수}}
}}"""

        try:
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()

            evaluation = json.loads(content)
            return evaluation

        except Exception as e:
            return {
                'score': 0,
                'feedback': f"평가 중 오류: {str(e)}",
                'strengths': [],
                'weaknesses': [],
                'suggestions': [],
                'rubric_scores': {}
            }
