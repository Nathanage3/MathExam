from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import Grade, Unit, Test, Question, Choice, TestAttempt

# Import serializers at the top to avoid circular imports
from .serializers import (
    GradeSerializer, UnitSerializer, TestSerializer, 
    QuestionSerializer, TestAttemptSerializer, SubmitTestSerializer
)

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all().order_by('order')
    serializer_class = GradeSerializer
    
    @action(detail=True, methods=['get'])
    def units(self, request, pk=None):
        grade = self.get_object()
        units = Unit.objects.filter(grade=grade).order_by('order')
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all().order_by('order')
    serializer_class = UnitSerializer
    
    def get_queryset(self):
        queryset = Unit.objects.all().order_by('order')
        grade_id = self.request.query_params.get('grade_id')
        if grade_id is not None:
            queryset = queryset.filter(grade_id=grade_id)
        return queryset
    
    @action(detail=True, methods=['get'])
    def tests(self, request, pk=None):
        unit = self.get_object()
        tests = Test.objects.filter(unit=unit).order_by('order')
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all().order_by('order')
    serializer_class = TestSerializer
    
    def get_queryset(self):
        queryset = Test.objects.all().order_by('order')
        unit_id = self.request.query_params.get('unit_id')
        if unit_id is not None:
            queryset = queryset.filter(unit_id=unit_id)
        return queryset
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        test = self.get_object()
        questions = Question.objects.filter(test=test).order_by('order')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        test = self.get_object()
        serializer = SubmitTestSerializer(data=request.data)
        
        if serializer.is_valid():
            student_name = serializer.validated_data['student_name']
            answers = serializer.validated_data['answers']
            
            score = 0
            total_questions = test.question_set.count()
            
            # Calculate score
            for question_id, choice_id in answers.items():
                try:
                    question = Question.objects.get(id=question_id, test=test)
                    choice = Choice.objects.get(id=choice_id, question=question)
                    if choice.is_correct:
                        score += 1
                except (Question.DoesNotExist, Choice.DoesNotExist):
                    pass
            
            # Save attempt
            attempt = TestAttempt.objects.create(
                test=test,
                student_name=student_name,
                score=score,
                total_questions=total_questions
            )
            
            return Response({
                'student_name': student_name,
                'test_name': test.name,
                'score': score,
                'total_questions': total_questions,
                'percentage': (score / total_questions) * 100 if total_questions > 0 else 0,
                'attempt_id': attempt.id
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        test = self.get_object()
        attempts = TestAttempt.objects.filter(test=test).order_by('-completed_at')[:10]
        serializer = TestAttemptSerializer(attempts, many=True)
        return Response(serializer.data)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('order')
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        queryset = Question.objects.all().order_by('order')
        test_id = self.request.query_params.get('test_id')
        if test_id is not None:
            queryset = queryset.filter(test_id=test_id)
        return queryset

class TestAttemptViewSet(viewsets.ModelViewSet):
    queryset = TestAttempt.objects.all().order_by('-completed_at')
    serializer_class = TestAttemptSerializer
    
    def get_queryset(self):
        queryset = TestAttempt.objects.all().order_by('-completed_at')
        test_id = self.request.query_params.get('test_id')
        student_name = self.request.query_params.get('student_name')
        
        if test_id is not None:
            queryset = queryset.filter(test_id=test_id)
        if student_name is not None:
            queryset = queryset.filter(student_name__icontains=student_name)
        
        return queryset

# Traditional HTML views
def home_page(request):
    return render(request, 'exams/home.html')

def take_test_page(request, test_id):
    return render(request, 'exams/take_test.html')

def test_result_page(request):
    return render(request, 'exams/test_result.html')