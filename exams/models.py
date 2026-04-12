from django.db import models
from django.contrib.auth.models import User

class Exam(models.Model):
    """Модель учебного экзамена."""
    title = models.CharField(max_length=200, verbose_name="Название экзамена")
    duration = models.PositiveIntegerField(
        help_text="Продолжительность в минутах", 
        verbose_name="Время на прохождение"
    )

    class Meta:
        verbose_name = "Экзамен"
        verbose_name_plural = "Экзамены"

    def __str__(self):
        return self.title

class Question(models.Model):
    """Вопросы, привязанные к конкретному экзамену."""
    exam = models.ForeignKey(
        Exam, 
        related_name='questions', 
        on_delete=models.CASCADE, 
        verbose_name="Экзамен"
    )
    text = models.TextField(verbose_name="Текст вопроса")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        # Обрезаем текст для админки, чтобы список был читаемым
        return self.text[:50] + '...' if len(self.text) > 50 else self.text

class Answer(models.Model):
    """Варианты ответов на вопросы."""
    question = models.ForeignKey(
        Question, 
        related_name='answers', 
        on_delete=models.CASCADE, 
        verbose_name="Вопрос"
    )
    text = models.CharField(max_length=200, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text

class Result(models.Model):
    """Результаты прохождения тестирования пользователями."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="Экзамен")
    test_species = models.CharField(
        max_length=200, 
        default='Входное тестирование', 
        verbose_name="Тип тестирования"
    )
    score = models.PositiveIntegerField(verbose_name="Полученный балл")
    date_taken = models.DateTimeField(auto_now_add=True, verbose_name="Дата прохождения")

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        # Сортировка: самые свежие результаты сверху
        ordering = ['-date_taken']

    def __str__(self):
        return f"{self.user.username} | {self.exam.title} | {self.score}"
