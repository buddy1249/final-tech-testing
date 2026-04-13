from django.contrib import admin
from .models import Exam, Question, Answer, Result

# Inline-редактирование ответов прямо внутри вопроса
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Сразу предлагаем 4 поля для ответов

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam')
    list_filter = ('exam',)
    search_fields = ('text',)
    inlines = [AnswerInline]  # Ответы создаются на той же странице, что и вопрос

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'get_questions_count')
    search_fields = ('title',)

    def get_questions_count(self, obj):
        return obj.questions.count()
    get_questions_count.short_description = "Количество вопросов"

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    # Поля, которые видны в общем списке
    list_display = ('user', 'exam', 'test_species', 'score', 'date_taken')
    # Фильтры справа
    list_filter = ('test_species', 'exam', 'date_taken')
    # Поиск по имени пользователя и названию теста
    search_fields = ('user__username', 'exam__title')
    # Поля только для чтения (чтобы нельзя было подделать результат в админке)
    readonly_fields = ('date_taken',)

