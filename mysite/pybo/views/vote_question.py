from ..forms import AnswerForm, QuestionForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Question, Answer, Comment
from django.contrib import messages 

def vote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.user == question.author:
        message(request, "주작 금지")
    else:
        question.voter.add(request.user)
    
    return redirect("pybo:detail", question_id=question_id)