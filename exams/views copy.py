from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, Answer, Result
import random
from django.utils import timezone
from datetime import datetime 
import datetime


def index(request):
    return render(request, 'exams/index.html')


def start_exam(request, exam_id):
    """Логика начала экзамена, возможно, c сохранением времени начала в сессии и БД """
    exam = get_object_or_404(Exam, id=exam_id)
    return redirect('take_exam', exam_id=exam.id)
   
    
@login_required
def take_exam(request, exam_id, exam2_id=1):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    genus = 'Входное тестирование' if exam2_id == 1 else 'Итоговое тестирование'
    
    print('fff:', genus)
    if request.method == 'POST':
        score = 0
        for question in questions:
            # Получаем выбранный пользователем ответ для данного вопроса
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                try:
                    selected_answer = Answer.objects.get(id=selected_answer_id)
                    if selected_answer.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    continue
        
        # Сохраняем результат       
        if str(request.user) in ['root', 'К.Н.Васильев', 'И.А.Виноградов', 'free_user']:
            Result.objects.create(user=request.user, exam=exam, score=score, test_species=genus)            
            return redirect('exam_results', exam_id=exam.id)
        elif str(request.user) not in ['root', 'К.Н.Васильев', 'И.А.Виноградов', 'free_user']:
            return render(request, 'exams/default.html')   
            #return HttpResponse(f'Тестирование доступно только авторизованным пользователям!')
        else:
            pass
    
    print(type(questions))
    questions = list(questions)
    # print(questions)
    questions = random.sample(questions, 5)
    for question in questions:
        for answer in question.answers.all():
            print(answer)
    
        
        
    return render(request, 'exams/take_exam.html', {'exam': exam, 'questions': questions, 'genus': genus})


def exam_results(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    result = Result.objects.filter(user=request.user, exam=exam).order_by('-date_taken').first()
    rr = Result.objects.all().order_by('-date_taken')
    for i in rr:
        print(i.user, i.exam, i.score,  i.date_taken.strftime('%Y-%m-%d'), i.test_species)
    day = timezone.now().strftime('%Y-%m-%d')
    print('Время, дата', day, type(day))
    
    date_taken = result.date_taken.strftime('%Y-%m-%d')
    return render(request, 'exams/exam_results.html', {'result': result, 'exam': exam, 'date_taken': date_taken})

# @login_required
def results_all(request):    
    result_all = Result.objects.all()
    # for i in result_all:
    #     print(i.id, i.user, i.date_taken, i.test_species, i.score)
    return render(request, 'exams/results_all.html', {'result_all': result_all})


def default(request):
    return render(request, 'exams/default.html')


