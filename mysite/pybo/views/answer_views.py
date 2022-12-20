from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..forms import AnswerForm, QuestionForm, CommentForm
from django.utils import timezone
from ..models import Question, Answer, Comment
from django.contrib import messages 

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

    return redirect('pybo:detail',  question_id=answer.question.id)
    