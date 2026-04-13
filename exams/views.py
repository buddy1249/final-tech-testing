import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from .models import Exam, Answer, Result

def index(request: HttpRequest) -> HttpResponse:
    """Рендеринг главной страницы сервиса тестирования."""
    return render(request, 'exams/index.html')

def start_exam(request: HttpRequest, exam_id: int) -> HttpResponse:
    """Инициализация начала тестирования."""
    exam = get_object_or_404(Exam, id=exam_id)
    return redirect('take_exam', exam_id=exam.id)

@login_required
def take_exam(request: HttpRequest, exam_id: int, exam2_id: int = 1) -> HttpResponse:
    """Логика прохождения тестирования с расчетом баллов."""
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    genus = 'Входное тестирование' if exam2_id == 1 else 'Итоговое тестирование'
    
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_id = request.POST.get(f'question_{question.id}')
            if selected_id:
                # Оптимизация: проверяем правильность одним запросом
                if Answer.objects.filter(id=selected_id, is_correct=True).exists():
                    score += 1
        
        # Вместо str(request.user) используем username и выносим в кортеж (быстрее поиск)
        ALLOWED_USERNAMES = ('root', 'П.П.Петров', 'И.И.Иванов', 'free_user')
        
        if request.user.username in ALLOWED_USERNAMES:
            Result.objects.create(
                user=request.user, 
                exam=exam, 
                score=score, 
                test_species=genus
            )
            return redirect('exam_results', exam_id=exam.id)
        
        return render(request, 'exams/default.html')
    
    """Добавляем защиту: min() для исключения падения random.sample 
       если вопросов в базе меньше 5
    """ 
    count = min(questions.count(), 5)
    sampled_questions = random.sample(list(questions), count) if count > 0 else []
    
    return render(request, 'exams/take_exam.html', {
        'exam': exam, 
        'questions': sampled_questions, 
        'genus': genus
    })

@login_required
def exam_results(request: HttpRequest, exam_id: int) -> HttpResponse:
    """Вывод итогового результата последнего теста."""
    exam = get_object_or_404(Exam, id=exam_id)
    result = Result.objects.filter(user=request.user, exam=exam).order_by('-date_taken').first()
    
    # Защита от случая, когда результата нет в БД
    if not result:
        return redirect('index')

    context = {
        'result': result, 
        'exam': exam, 
        'date_taken': result.date_taken.strftime('%Y-%m-%d')
    }
    return render(request, 'exams/exam_results.html', context)

#@login_required
def results_all(request: HttpRequest) -> HttpResponse:
    """Общий протокол тестирования (доступен только авторизованным, кроме демо)."""    
    result_all = Result.objects.select_related('user', 'exam').all() # Оптимизация запроса   
    return render(request, 'exams/results_all.html', {'result_all': result_all})

def default(request: HttpRequest) -> HttpResponse:
    """Страница заглушка/отказа в доступе."""
    return render(request, 'exams/default.html')
