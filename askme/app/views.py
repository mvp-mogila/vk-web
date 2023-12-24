from django.forms import model_to_dict
from django.http import HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse

from app.models import Question, Profile, Reaction, Tag, Answer
from app.forms import LoginForm, ProfileForm, RegistrationForm, AskForm, AnswerForm


def index_handler(request):
    page = request.GET.get('page', 1)
    questions = Question.objects.new()
    if (not questions):
        return HttpResponseNotFound()
    context = {'title': 'New questions', 'objects': paginate(questions, page)}
    return render(request, 'index.html', context)


@csrf_protect
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


@csrf_protect
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


@csrf_protect
def profile_handler(request, username):
    profile = Profile.objects.profile_by_username(username)
    if (request.user.username == username):
        if (request.method == 'GET'):
            profile_form = ProfileForm(initial=model_to_dict(request.user))
            context = {'owner': True, 'profile_form': profile_form, 'profile': profile}

        if (request.method == 'POST'):
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
            if (profile_form.is_valid()):
                profile_form.save()
                return redirect(reverse('profile', args=[username]))
    else:
        context = {'owner': False, 'profile': profile}

    return render(request, 'profile.html', context)


@login_required
@csrf_protect
def logout_handler(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
@csrf_protect
def ask_handler(request):
    if (request.method == 'GET'):
        ask_form = AskForm()
    
    if (request.method == 'POST'): # ? superuser creation
        ask_form = AskForm(request.POST)
        if (ask_form.is_valid()):
            author = request.user.profile
            new_question = ask_form.save(author)
            author.add_question()
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


@csrf_protect
def question_handler(request, question_id):
    page = request.GET.get('page', 1)
    question = Question.objects.get_by_id(question_id)
    if (not question):
        return HttpResponseNotFound()
    answers = question.answer.all()
    
    if (not request.user.is_anonymous and request.user.profile == question.author):
        owner = True
    else:
        owner = False

    if (request.method == 'GET'):
        answer_form = AnswerForm()
    
    if (request.method == 'POST'):
        if (request.user.is_anonymous):
            return redirect(reverse('login'))

        answer_form = AnswerForm(request.POST)
        if (answer_form.is_valid()):
            author = request.user.profile
            answer_form.save(author, question)
            author.add_answer()
            new_page = Paginator(question.answer.all(), 3).num_pages
            return redirect(reverse('question', args=[question_id]) + f'?page={new_page}')

    context = {'question': question, 'objects': paginate(answers, page), 'answer_form': answer_form, 'owner': owner}
    return render(request, 'question.html', context)


@csrf_protect
def answer_vote_handler(request):
    if (request.user.is_anonymous):
        return JsonResponse({'error': 1, 'message': 'You have to login for voting!'})
    
    answer_id = request.POST.get('answer_id')
    positive = request.POST.get('positive')
    answer = get_object_or_404(Answer, id=answer_id)
    if (answer.author != request.user.profile):
        rating = Reaction.objects.add_reaction(author=request.user.profile, object=answer, positive=positive)
    else:
        return JsonResponse({'error': 1, 'message': 'You can\'t rate self-created objects!'})
    return JsonResponse({'error': 0, 'rating': rating})


@csrf_protect
def question_vote_handler(request):
    if (request.user.is_anonymous):
        return JsonResponse({'error': 1, 'message': 'You have to login for voting!'})
    
    question_id = request.POST.get('question_id')
    positive = request.POST.get('positive')
    question = get_object_or_404(Question, id=question_id)
    if (question.author != request.user.profile):
        rating = Reaction.objects.add_reaction(author=request.user.profile, object=question, positive=positive)
    else:
        return JsonResponse({'error': 1, 'message': 'You can\'t rate self-created objects!'})
    return JsonResponse({'error': 0, 'rating': rating})


@csrf_protect
def answer_correct(request):
    if (request.user.is_anonymous):
        return JsonResponse({'error': 1, 'message': 'You have to login to mark answers!'})
    
    answer_id = request.POST.get('answer_id')
    answer = get_object_or_404(Answer, id=answer_id)
    errmessage = answer.mark_correct()
    return JsonResponse({'error': 0, 'message': errmessage})



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