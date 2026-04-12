menu = [{'title':'главная'},{'title':'Смена'}, {'title':'Отчет в ДС_куку'}, {'title':'Селектор'}, 
        {'title':'our money'}, {'title':'Войти'}, {'title':'Выйти'}]


def get_agnks_context(request):
    return {'mainmenu': menu}