from django.http import HttpResponseNotFound, Http404
from django.shortcuts import redirect, render
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from app.models import Question, Profile, Tag
from app.forms import LoginForm, RegistrationForm, AskForm


def index_handler(request):
    page = request.GET.get('page', 1)
    questions = Question.objects.new()
    if (not questions):
        return HttpResponseNotFound()
    context = {'title': 'New questions', 'objects': paginate(questions, page)}
    return render(request, 'index.html', context)


def signup_handler(request):
    if (request.method == 'GET'):
        registration_form = RegistrationForm()

    if (request.method == 'POST'):
        registration_form = RegistrationForm(request.POST)
        if (registration_form.is_valid()):
            new_user = registration_form.save() # TODO profile_picture
            Profile.objects.create(user = new_user, profile_pic = registration_form.cleaned_data['profile_picture'])

    context = {'registration_form': registration_form}
    return render(request, 'signup.html', context)


def login_handler(request):
    if (request.method == 'GET'):
        login_form = LoginForm()
        error = False

    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if (login_form.is_valid()):
            user = authenticate(request, **login_form.cleaned_data)
            if (user):
                login(request, user)
                return redirect(reverse('index'))
            else:
                login_form = LoginForm()
                error = True

    context = {'login_form': login_form, 'error': error}
    return render(request, 'login.html', context)


@login_required
def logout_handler(request):
    logout(request)
    return redirect(reverse('login'))


def ask_handler(request):
    if (request.method == 'GET'):
        ask_form = AskForm()
    
    if (request.method == 'POST'):  # ? supeuser creation
        ask_form = AskForm(request.POST)
        if (ask_form.is_valid()):
            new_question = ask_form.save(commit=False)
            new_question.author = request.user.profile
            new_question.save()
            tags_list = ask_form.cleaned_data['tags']
            for tag in tags_list:
                question_tag = Tag.objects.create_or_get_tag(tag)
                new_question.tags.add(question_tag)
            new_question.save()
            return redirect(reverse('question', args=[new_question.id]))

    context = {'ask_form': ask_form}
    return render(request, 'ask.html', context)


def tag_handler(request, tag_name):
    page = request.GET.get('page', 1)
    questions = Question.objects.questions_by_tag(tag_name)
    if (not questions):
        return HttpResponseNotFound()
    context = {'title': f"Questions by tag \"{tag_name}\"", 'objects': paginate(questions, page)}
    return render(request, 'index.html', context)


def question_handler(request, question_id):
    page = request.GET.get('page', 1)
    question = Question.objects.get_by_id(question_id)
    if (not question):
        return HttpResponseNotFound()
    answers = question.answer.all()
    context = {'question': question, 'objects': paginate(answers, page)}
    return render(request, 'question.html', context)


def new_questions_handler(request):
    page = request.GET.get('page', 1)
    questions = Question.objects.new()
    if (not questions):
        return HttpResponseNotFound()
    context = {'title': 'New questions', 'objects': paginate(questions, page)}
    return render(request, 'index.html', context)


def hot_questions_handler(request):
    page = request.GET.get('page', 1)
    questions = Question.objects.hot()
    if (not questions):
        return HttpResponseNotFound()
    context = {'title': 'Top questions', 'objects': paginate(questions, page)}
    return render(request, 'index.html', context)


def paginate(objects, page_num, per_page = 3):
    paginator = Paginator(objects, per_page)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        raise SuspiciousOperation('Invalid request')
    except EmptyPage:
        raise Http404()
    page.adjusted_elided_pages = paginator.get_elided_page_range(page_num, on_ends=1, on_each_side=2)
    return page