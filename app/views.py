from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.models import Question, Answer, Profile, RatingQuestions
from django.template.defaulttags import register
from django.contrib import auth
from blog.forms import LoginForm, AskForm, RegisterForm, SettingsForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from pprint import pformat
#from django.views.decoration 


# Create your views here.


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

num=2


def login(request):
    if request.method =='GET':
        form = LoginForm()
        next_page = request.GET.get('next','') 
        request.session['next_page'] = next_page
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                # request.session['hello']= 'world'
                # доставать request.session.pop('hello')
                # после логина предыдущая страница добавить
                auth.login(request, user)
                next_page = request.session.pop('next_page')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('home') 
        
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    page = request.META.get('HTTP_REFERER') # чет на другое поменять
    return redirect(page)


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def ask(request):
    if request.method == 'GET':
        data_dict={}
        form = AskForm()
    else:
        form = AskForm(request.POST, profile=request.user.profile) 
        if form.is_valid():
            question = form.save()
            return redirect(reverse('question', kwargs={'question_id': question.pk}))
    return render(request, 'ask.html', {'form': form})



def hot(request):
    questions = Question.objects.all()
    massiv = {}
    for question in questions:
        massiv[question.id] = Answer.objects.count(question.id)
    questions = pages(questions, num, request)
    return render(request, 'hot.html', {'elems': questions, 'nums': massiv})



def tag(request, tag):
    questions = Question.objects.find_tag(tag)
    nums={}
    for question in questions:
        nums[question.id] = Answer.objects.count(question.id)
    questions = pages(questions, num, request)
    return render(request, 'tag.html', {'tag': tag, 'elems': questions, 'nums': nums})


def index(request):

    print('\n\n', '='*100)
    print(f'HELLO: {request.session.get("hello")}')
    print('\n\n', '='*100)

    questions = Question.objects.all()
    nums = {}
    for question in questions:
        nums[question.id] = Answer.objects.count(question.id)
    questions = pages(questions, 2, request)
    return render(request, 'index.html', {'elems': questions, 'nums': nums})

@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(initial={'username': request.user.username, 
            'email': request.user.profile.email, 
            'avatar': request.user.profile.avatar, 
            'nickname': request.user.profile.nickname,}, user=request.user)
    else:
        form = SettingsForm(request.POST, instance=request.user.profile, user=request.user, files=request.FILES)
        if form.is_valid():
            profile = form.save()
            return redirect('settings')
    return render(request, 'settings.html', {'form': form})


def question(request, question_id):
    question = Question.objects.find_id(question_id)
    answers = pages(Answer.objects.find_by_q(question_id), num, request)
    if request.method == 'GET':
        form = AnswerForm()
        answers = pages(Answer.objects.find_by_q(question_id), num, request)
    else:
        form = AnswerForm(data=request.POST, qid=question, profile=request.user.profile)
        if form.is_valid():
            answer = form.save()
            return redirect(reverse('question', kwargs={'question_id': question.pk}))
    return render(request, 'question.html', {'elems': answers, 'question': question, 'form': form})


def pages(elems, num_per_page, request, page_num=1):
    paginator = Paginator(elems, num_per_page) # Show 2
    page = request.GET.get('page', page_num)
    elems = paginator.get_page(page)
    return elems

@require_POST
@login_required
def vote(request):
    data = request.POST
    qid = data['qid']
    action = data['action']
    user = request.user.profile
    # обработка лайков
    rate = RatingQuestions.objects.find_eu(qid, user)
    if not rate:
        new_rate = RatingQuestions.objects.change_rate(qid, user, action)
        response = {"response": new_rate, "success": True}
    else:
        response = {"response": 0, "success": False}
    return JsonResponse(response)