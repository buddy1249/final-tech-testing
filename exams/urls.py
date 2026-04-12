from django.urls import path, re_path 
from . import views

urlpatterns = [    
    path('', views.index, name="home"), 
    path('start/<int:exam_id>/', views.start_exam, name='start_exam'),
    path('take/<int:exam_id>/<int:exam2_id>/', views.take_exam, name='take_exam'),
    path('results/<int:exam_id>/', views.exam_results, name='exam_results'),
    path('results_all/', views.results_all, name='results_all'),    
    path('default/', views.default, name='default'),      
    
] 





# Примеры
# path('year/', views.year, name="year"),
    # path('month/<str:month>', views.month, name="month"),
    # path('month_sum/<int:month>', views.month_sum, name="month_sum"),
    # path('day/<str:day>', views.day, name="day"),    
    # path("archive/<year4:year>/", views.archive),