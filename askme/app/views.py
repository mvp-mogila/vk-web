from django.http import HttpRequest, HttpResponse 
from django.shortcuts import render
from django.core.paginator import Paginator


QUESTIONS = [
        {
            'id': i,
            'title': f"Title {i}",
            'user': f"User {i}",
            'datetime': '01.01.2023 10:10',
            'content': f"Some text {i} ?",
            'rating': i * 2,
            'tags': [f"tag {j}" for j in range(3)]
        } for i in range(10)
    ]


ANSWERS = [
    {
        'id': i,
        'user': f"User {i}",
        'datetime': '01.01.2023 10:11',
        'content': f"Some text {i}",
        'rating': i * 3,
        'correct': True
    } for i in range(3)
]


def index_handler(request):
    page = request.GET.get('page')
    if (not page):
        page = 1
    context = {'title': 'New questions', 'questions': paginate(QUESTIONS, page)}
    return render(request, "index.html", context)


def signup_handler(request):
    return render(request, "signup.html")


def login_handler(request):
    return render(request, "login.html")


def ask_handler(request):
    return render(request, "ask.html")


def tag_handler(request, tag_name):
    page = request.GET.get('page')
    if (not page):
        page = 1
    context = {'title': f"Questions by tag \"{tag_name}\"", 'questions': paginate(QUESTIONS, page)}
    return render(request, "index.html", context)


def question_handler(request, question_id):
    page = request.GET.get('page')
    if (not page):
        page = 1
    if (question_id > 5):
        context = {'question': QUESTIONS[question_id], 'answers': paginate(ANSWERS, page)}
    else:
        context = {'question': QUESTIONS[question_id]}
    return render(request, "question.html", context)


def hot_question_handler(request):
    context = {'title': 'Top questions', 'questions': [ QUESTIONS[9], QUESTIONS[8] ]}
    return render(request, "index.html", context)


def paginate(objects, page, per_page = 3):
    paginator = Paginator(objects, per_page)
    return paginator.page(page)