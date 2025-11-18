"""
Views for AI tutor functionality
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync

from .models import Conversation, Message, PracticeQuestion, StudentAnswer
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    PracticeQuestionSerializer,
    StudentAnswerSerializer
)
from .tutor import AITutor
from courses.models import Course, Lesson
from users.models import StudentProfile


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for AI tutor conversations"""

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only show user's own conversations"""
        return Conversation.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        """Create conversation for current user"""
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['post'])
    def ask(self, request, pk=None):
        """Ask a question to the AI tutor"""
        conversation = self.get_object()
        question = request.data.get('question')

        if not question:
            return Response(
                {'error': 'Question is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if student can use AI tutor
        try:
            profile = request.user.student_profile
            if not profile.can_use_ai_tutor():
                return Response(
                    {'error': 'AI tutor limit reached. Upgrade to Pro for unlimited access.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except StudentProfile.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get conversation history
        messages = conversation.messages.all()
        conversation_history = [
            {'role': msg.role, 'content': msg.content}
            for msg in messages
        ]

        # Build context
        course_context = ""
        lesson_context = ""

        if conversation.course:
            course_context = f"코스: {conversation.course.title}\n설명: {conversation.course.description}"

        if conversation.lesson:
            lesson_context = f"레슨: {conversation.lesson.title}\n내용: {conversation.lesson.content}"

        # Get student profile data
        student_profile_data = {
            'learning_level': profile.user.learning_level,
            'learning_style': profile.user.learning_style,
            'weak_areas': profile.weak_topics,
            'performance': {
                'avg_quiz_score': profile.average_quiz_score,
                'avg_assignment_score': profile.average_assignment_score,
            }
        }

        # Create AI tutor and get answer
        tutor = AITutor(
            course_context=course_context,
            student_profile=student_profile_data
        )

        # Call async function synchronously
        result = async_to_sync(tutor.answer_question)(
            question=question,
            lesson_context=lesson_context,
            conversation_history=conversation_history
        )

        if not result['success']:
            return Response(
                {'error': result.get('error', 'Failed to get answer')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save messages
        user_message = Message.objects.create(
            conversation=conversation,
            role='user',
            content=question
        )

        assistant_message = Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=result['answer'],
            tokens_used=result['tokens_used'],
            model_used=result['model']
        )

        # Update student profile
        profile.ai_questions_asked += 1
        profile.save()

        # Update conversation title if first message
        if not conversation.title:
            conversation.title = question[:100]
            conversation.save()

        return Response({
            'question': MessageSerializer(user_message).data,
            'answer': MessageSerializer(assistant_message).data
        })

    @action(detail=False, methods=['post'])
    def start_conversation(self, request):
        """Start a new conversation"""
        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')

        conversation = Conversation.objects.create(
            student=request.user,
            course_id=course_id if course_id else None,
            lesson_id=lesson_id if lesson_id else None
        )

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )


class PracticeQuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for practice questions"""

    serializer_class = PracticeQuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter by course or lesson if specified"""
        queryset = PracticeQuestion.objects.all()

        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        lesson_id = self.request.query_params.get('lesson_id')
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)

        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        return queryset

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate new practice questions using AI"""
        topic = request.data.get('topic')
        difficulty = request.data.get('difficulty', 'medium')
        count = int(request.data.get('count', 5))
        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')

        if not topic:
            return Response(
                {'error': 'Topic is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get course context
        course_context = ""
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            course_context = f"{course.title}: {course.description}"

        # Create AI tutor
        tutor = AITutor(course_context=course_context)

        # Generate questions
        questions = async_to_sync(tutor.generate_practice_questions)(
            topic=topic,
            difficulty=difficulty,
            count=count
        )

        # Save questions to database
        saved_questions = []
        for q_data in questions:
            question = PracticeQuestion.objects.create(
                course_id=course_id,
                lesson_id=lesson_id if lesson_id else None,
                topic=topic,
                difficulty=difficulty,
                question=q_data['question'],
                options=q_data.get('options'),
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation']
            )
            saved_questions.append(question)

        serializer = self.get_serializer(saved_questions, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentAnswerViewSet(viewsets.ModelViewSet):
    """ViewSet for student answers"""

    serializer_class = StudentAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only show user's own answers"""
        return StudentAnswer.objects.filter(student=self.request.user)

    @action(detail=False, methods=['post'])
    def submit(self, request):
        """Submit and evaluate an answer"""
        question_id = request.data.get('question_id')
        answer = request.data.get('answer')

        if not question_id or not answer:
            return Response(
                {'error': 'question_id and answer are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        question = get_object_or_404(PracticeQuestion, id=question_id)

        # Create AI tutor for evaluation
        tutor = AITutor()

        # Evaluate answer
        evaluation = async_to_sync(tutor.evaluate_answer)(
            question=question.question,
            student_answer=answer,
            correct_answer=question.correct_answer
        )

        # Save student answer
        student_answer = StudentAnswer.objects.create(
            student=request.user,
            question=question,
            answer=answer,
            is_correct=evaluation['is_correct'],
            ai_feedback=evaluation['feedback'],
            score=evaluation['score'],
            evaluation_criteria=evaluation
        )

        # Update question stats
        question.times_used += 1
        if evaluation['is_correct']:
            question.times_correct += 1
        question.save()

        # Update student profile
        try:
            profile = request.user.student_profile
            # You could update average scores here
            profile.save()
        except StudentProfile.DoesNotExist:
            pass

        return Response(StudentAnswerSerializer(student_answer).data)
