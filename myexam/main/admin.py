from django.contrib import admin
from .models import Grade, Unit, Test, Question, Choice, TestAttempt

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['test', 'order', 'question_preview']
    list_filter = ['test__unit__grade', 'test']  # Filter by grade and test
    search_fields = ['question_text']
    
    def question_preview(self, obj):
        return obj.question_text[:75] + "..." if len(obj.question_text) > 75 else obj.question_text
    question_preview.short_description = 'Question'

class TestAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'get_grade']
    list_filter = ['unit__grade', 'unit']
    
    def get_grade(self, obj):
        return obj.unit.grade.name
    get_grade.short_description = 'Grade'

admin.site.register(Grade)
admin.site.register(Unit)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(TestAttempt)