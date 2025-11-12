from rest_framework import serializers
from .models import Grade, Unit, Test, Question, Choice, TestAttempt

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'order', 'question_text', 'choices']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'order', 'total_questions', 'questions']

class UnitSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, read_only=True)
    
    class Meta:
        model = Unit
        fields = ['id', 'name', 'order', 'tests']

class GradeSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    
    class Meta:
        model = Grade
        fields = ['id', 'name', 'order', 'units']

class TestAttemptSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.name', read_only=True)
    
    class Meta:
        model = TestAttempt
        fields = ['id', 'test', 'test_name', 'student_name', 'score', 'total_questions', 'completed_at']

class SubmitTestSerializer(serializers.Serializer):
    student_name = serializers.CharField(max_length=100)
    answers = serializers.DictField(
        child=serializers.IntegerField()
    )