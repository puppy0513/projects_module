from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail , name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name = 'question_create'),
    #path('finance/', views.finance, name = 'finance'),
    #path('finance/<int:finance_id>/', views.finance_detail, name = 'finance_detail'),
    path('kospi/', views.kospi , name = 'kospi'),
    path('kosdaq/', views.kosdaq , name = 'kosdaq'),
    path('kospi/<int:kospi_id>/', views.kospi_detail , name = 'kospi_detail'),
    path('kosdaq/<int:kosdaq_id>/', views.kosdaq_detail , name = 'kosdaq_detail'),    
    path('kospi/<int:id>/graph', views.graph , name = 'graph'),
    path('kosdaq/<int:id>/graph', views.graph , name = 'graph'),
]