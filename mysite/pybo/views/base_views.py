from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from ..models import Question
from django.db.models import Q, Count

# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    kw = request.GET.get('kw', '')
    condition = request.GET.get('condition', '')
    so = request.GET.get('so', 'recent')
 
    if so == 'recommend':
        question_list= Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list= Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')
 
    print(condition)
 
    # question_list = Question.objects.order_by('-create_date')
   
    if kw:
        if condition == 'title':
            question_list = question_list.filter(    
                Q(subject__icontains=kw) ).distinct()
        elif condition == 'content':
            question_list = question_list.filter(    
                Q(content__icontains=kw) ).distinct()
        elif condition == 'author':
            question_list = question_list.filter(    
                Q(author__username__icontains=kw) ).distinct()
        elif condition == 'answer_author':
            question_list = question_list.filter(    
                Q(answer__author__username__icontains=kw) ).distinct()
 
    print(question_list)
    
    # 페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {"question_list" : page_obj, 'page' : page, 'kw':kw, 'condition' : condition, 'so':so}
    return render(request, 'pybo/question_list.html', context)

@login_required(login_url='common:login')
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'pybo/question_detail.html', {'question' : question})
