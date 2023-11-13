from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Tag


def index_handler(request):
    page = request.GET.get('page', 1)
    questions = Question.objects.new()
    if (not questions):
        return HttpResponseNotFound()
    context = {'title': 'New questions', 'objects': paginate(questions, page)}
    return render(request, "index.html", context)


def signup_handler(request):
    return render(request, "signup.html")


def login_handler(request):
    return render(request, "login.html")


def ask_handler(request):
    return render(request, "ask.html")


def tag_handler(request, tag_name):
    page = request.GET.get('page', 1)
    questions = Tag.objects.questions_by_tag(tag_name)
    if (not questions):
        return HttpResponseNotFound()
    context = {'title': f"Questions by tag \"{tag_name}\"", 'objects': paginate(questions, page)}
    return render(request, "index.html", context)


def question_handler(request, question_id):
    page = request.GET.get('page', 1)
    question = Question.objects.get_by_id(question_id)
    if (not question):
        return HttpResponseNotFound()
    answers = question.answer.all()
    context = {'question': question, 'objects': paginate(answers, page)}
    return render(request, "question.html", context)


def hot_question_handler(request):
    page = request.GET.get('page', 1)
    questions = Question.objects.hot()
    if (not questions):
        return HttpResponseNotFound()
    context = {'title': 'Top questions', 'objects': paginate(questions, page)}
    return render(request, "index.html", context)


def paginate(objects, page_num, per_page = 3):
    paginator = Paginator(objects, per_page)
    # try:
    page = paginator.page(page_num)
    # except PageNotAnInteger:
    #     raise HttpResponseBadRequest()
    # except EmptyPage:
    #     raise HttpResponseNotFound()
    return page