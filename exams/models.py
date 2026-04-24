from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Exam(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField(help_text="Продолжительность в минутах")

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    test_species = models.CharField(max_length=200, default='Входное тестирование') # Итоговое или входное тестирование
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exam.title} - {self.score}"