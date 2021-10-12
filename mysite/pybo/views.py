from datetime import datetime
from datetime import time
from django.shortcuts import get_object_or_404, render,get_list_or_404, redirect,HttpResponse
from django.utils import timezone
from numpy import datetime64, datetime_as_string
from .models import Question ,Finance, Kospi,Kosdaq
from .forms import QuestionForm, AnswerForm 
from django.core.paginator import Paginator
import FinanceDataReader as fdr
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components
import jinja2
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
import string
import json

def index(request):
    
    #pybo 목록 출력
    
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지

    question_list = Question.objects.order_by('-create_date')
    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    
    #pybo 내용 출력
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)  
    
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form= QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)

def finance(request):
    
    page = request.GET.get('page', '1') 

    finance_list = Finance.objects.order_by('-Date')
    paginator = Paginator(finance_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'finance_list': page_obj}
    return render(request,'pybo/finance_list.html',context)         #pybo/finance_list.html에 context 변수를 적용해서 넘겨줘라 
"""
def finance_detail(request,finance_id):
    finance_list = Finance.objects.get(id = finance_id)
    context ={'finance_list':finance_list}
    return render(request,'pybo/finance_detail.html',context)
"""
def kospi(request):

    page = request.GET.get('page', '1') 

    kospi_list = Kospi.objects.order_by('Symbol')
    paginator = Paginator(kospi_list, 20)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'kospi_list': page_obj}
    return render(request,'pybo/kospi.html',context)

def kosdaq(request):
    page = request.GET.get('page', '1') 

    kosdaq_list = Kosdaq.objects.order_by('Symbol')
    paginator = Paginator(kosdaq_list, 20)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'kosdaq_list': page_obj}
    return render(request,'pybo/kosdaq.html',context)


def kospi_detail(request,kospi_id):
    # 종목 정보
    Kospi_list = Kospi.objects.get(Symbol = kospi_id)

    kospi_id =str(kospi_id)
    # 종목 historic data
    if len(kospi_id) != 6:
        kospi_id = kospi_id.zfill(6)

    df = fdr.DataReader(kospi_id,'2021-09-01')
    #차트 그리기
    
    #데이터 형 변환
    df.index = df.index.astype(str)
    df['Change'] *= 100
  
    # json 데이터로 변형
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    
    #페이지 설정
    page = request.GET.get('page', '1') 
    paginator = Paginator(df, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context ={'Kospi_list':Kospi_list ,'d': data}
    return render(request,'pybo/kospi_detail.html',context)


def kosdaq_detail(request,kosdaq_id):
   # 종목 정보
    Kosdaq_list = Kosdaq.objects.get(Symbol = kosdaq_id)

    kosdaq_id =str(kosdaq_id)
    # 종목 historic data
    if len(kosdaq_id) != 6:
        kosdaq_id = kosdaq_id.zfill(6)

    df = fdr.DataReader(kosdaq_id,'2021-09-01')

    #데이터 형 변환
    df.index = df.index.astype(str)
    df['Change'] *= 100
  
    # json 데이터로 변형
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    
    #페이지 설정
    page = request.GET.get('page', '1') 
    paginator = Paginator(df, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context ={'Kosdaq_list':Kosdaq_list ,'d': data}
    return render(request,'pybo/kosdaq_detail.html',context)

def graph(request, id):
    id =str(id)   

    if len(id) != 6:
        id = id.zfill(6)
    
    df = fdr.DataReader(id,'2021-01-01')
    df = df.rename_axis('Date').reset_index()
    
    plot = figure(x_axis_type='datetime', plot_width=1000, plot_height=500)
    plot.line(df['Date'], df['Close'],color="navy", alpha=1,line_width = 3)
    script, div = components(plot)
 
    return render(request, 'pybo/graph.html', {'script': script, 'div': div})

