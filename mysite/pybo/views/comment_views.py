from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..forms import AnswerForm, QuestionForm, CommentForm
from django.utils import timezone
from ..models import Question, Answer, Comment
from django.contrib import messages 

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