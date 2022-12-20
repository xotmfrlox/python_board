import re
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Answer, Comment
from django.utils import timezone
from .forms import AnswerForm, QuestionForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

# Create your views here.
def index(request):
    page = request.GET.get('page', 1)

    question_list = Question.objects.order_by('-create_date')

    # 페이징 처리 
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {"question_list" : page_obj}
    return render(request, 'pybo/question_list.html', context)

@login_required(login_url='common:login')
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'pybo/question_detail.html', {'question' : question})

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    print(request.method)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")
    else:
        form = QuestionForm()
    
    context =  {'form' : form}
    
    return render(request, 'pybo/question_form.html',context) 

    

def question_modify(request, question_id ):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, "수정권한이 없습니다. ")
        return redirect('pybo:detail', question=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'pybo/question_form.html', {'form' : form})



def question_delete(request, question_id ):
    question = get_object_or_404(Question, pk=question_id)

    # 글쓴이가 본인글이 아닐때.... 
    if request.user != question.author:
        messages.error(request, "삭제권한 없음")
        return redirect('pybo:detail', question_id=question.id)
    
    question.delete()
    return redirect('pybo:index')


def answer_modify(request, answer_id):
    print("==========================================")
    print(f"answer_modify : {request.method}")
    answer = get_object_or_404(Answer, pk=answer_id)
    if answer.author != request.user:
        messages.error(request, "수정권한 없음")
        return redirect('pybo:detail', question_id = answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id = answer.question.id)
    else:
        form = AnswerForm(instance=answer)         

    return render(request, 'pybo/answer_form.html', {'answer' :answer, 'form' : form})


def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    # 글쓴이가 본인글이 아닐때.... 
    if request.user != answer.author:
        messages.error(request, "삭제권한 없음")
    else:
        answer.delete()

    return redirect('pybo:detail', question_id=answer.question.id)


def comment_create(request, question_id):
    question = get_object_or_404(Question, pk = question_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question 
            comment.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        form = CommentForm()

    return render(request, 'pybo/comment_form.html', {'form' : form})

def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk = comment_id)

    if request.user != comment.author:
        messages(request, "댓글수정권한이 없습니다.")
        return redirect('pybo:detail', question_id = comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id = comment.question.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'pybo/comment_form.html', {'form' : form})

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk = comment_id)

    if request.user != comment.author:
        messages(request, "댓글삭제권한이 없습니다.")
        return redirect('pybo:detail', question_id = comment.question.id)
    else:
        comment.delete()

    return redirect('pybo:detail', question_id = comment.question.id)


def comment_create_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk = answer_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id = comment.answer.question.id)
    else:
        form = CommentForm()

    return render(request, 'pybo/comment_form.html', {'form' : form})


def comment_modify_answer(request, comment_id ):
    comment = get_object_or_404(Comment, pk = comment_id)

    if request.user != comment.author:
        messages(request, "댓글수정권한이 없습니다.")
        return redirect('pybo:detail', question_id = comment.answer.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id = comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'pybo/comment_form.html', {'form' : form})

def comment_delete_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk = comment_id)

    if request.user != comment.author:
        messages(request, "댓글삭제권한이 없습니다.")
        return redirect('pybo:detail', question_id = comment.answer.question.id)
    else:
        comment.delete()

    return redirect('pybo:detail', question_id = comment.answer.question.id)
