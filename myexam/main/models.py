from django.db import models
from django.contrib.auth.models import User

class Grade(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.name)  # Ensure it returns a string
    
    class Meta:
        ordering = ['order']

class Unit(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        if self.grade and self.name:
            return f"{self.grade.name} - {self.name}"
        return str(self.name) if self.name else "Unnamed Unit"
    
    class Meta:
        ordering = ['order']

class Test(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=10)
    
    def __str__(self):
        if self.unit and self.unit.grade and self.name:
            return f"{self.unit.grade.name} - {self.unit.name} - {self.name}"
        return str(self.name) if self.name else "Unnamed Test"
    
    class Meta:
        ordering = ['order']

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.TextField()
    order = models.IntegerField(default=0)
    
    def __str__(self):
        if self.question_text:
            # Limit the length to avoid admin issues
            text = self.question_text[:50] + "..." if len(self.question_text) > 50 else self.question_text
            return f"Q{self.order}: {text}"
        return f"Question {self.id}"
    
    class Meta:
        ordering = ['order']

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        if self.choice_text:
            text = self.choice_text[:30] + "..." if len(self.choice_text) > 30 else self.choice_text
            return f"{text} {'✓' if self.is_correct else ''}"
        return f"Choice {self.id}"
    
    class Meta:
        ordering = ['id']

class TestAttempt(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.student_name and self.test:
            return f"{self.student_name} - {self.test.name} - {self.score}/{self.total_questions}"
        return f"Attempt {self.id}"
    
    class Meta:
        ordering = ['-completed_at']