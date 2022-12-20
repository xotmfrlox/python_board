from ..forms import AnswerForm, QuestionForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Question, Answer, Comment
from django.contrib import messages 

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