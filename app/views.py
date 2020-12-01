from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.models import Question, Answer, Profile
from django.template.defaulttags import register
from django.contrib import auth
from blog.forms import LoginForm, AskForm, RegisterForm, SettingsForm, AnswerForm
from django.contrib.auth.decorators import login_required
from pprint import pformat


# Create your views here.


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



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
                request.session['hello']= 'world'
                # доставать request.session.pop('hello')
                auth.login(request, user)
                next_page = request.session.pop('next_page')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('home') 
        
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    page = request.META.get('HTTP_REFERER')
    return redirect(page)

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.nickname = form.cleaned_data.get('nickname')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=user.username, password=raw_password)
            auth.login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.save()
            form.save_m2m()
            return redirect(reverse('question', kwargs={'question_id': question.pk}))
    return render(request, 'ask.html', {'form': form})



def hot(request):
    questions = Question.objects.all()
    massiv = {}
    for question in questions:
        massiv[question.id] = Answer.objects.count(question.id)
    paginator = Paginator(questions, 2) # Show 2
    page = request.GET.get('page', 1)
    questions = paginator.get_page(page)
    return render(request, 'hot.html', {'questions': questions, 'nums': massiv})



def tag(request, tag):
    questions = Question.objects.find_tag(tag)
    nums={}
    for question in questions:
        nums[question.id] = Answer.objects.count(question.id)
    paginator = Paginator(questions, 2) # Show 2
    page = request.GET.get('page', 1)
    questions = paginator.get_page(page)
    return render(request, 'tag.html', {'tag': tag, 'questions': questions, 'nums': nums})

def listing(request):

    print('\n\n', '='*100)
    print(f'HELLO: {request.session.get("hello")}')
    print('\n\n', '='*100)

    questions = Question.objects.all()
    nums = {}
    for question in questions:
        nums[question.id] = Answer.objects.count(question.id)
    paginator = Paginator(questions, 2) # Show 2
    page = request.GET.get('page', 1)
    questions = paginator.get_page(page)
    return render(request, 'index.html', {'elems': questions, 'nums': nums})

@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(initial={'username': request.user.username, 
            'email': request.user.profile.email, 
            'avatar': request.user.profile.avatar, 
            'nickname': request.user.profile.nickname })
    else:
        form = SettingsForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            request.user.username = form.cleaned_data.get('username')
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            profile.save()
            request.user.save()
            return redirect('settings')
    return render(request, 'settings.html', {'form': form})


def question(request, question_id):
    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.profile
            answer.question = Question.objects.find_id(question_id)
            answer.save()
    question = Question.objects.find_id(question_id)
    answers = Answer.objects.find_by_q(question_id)
    paginator = Paginator(answers, 2) # Show 2
    page = request.GET.get('page', 1)
    answers = paginator.get_page(page)
    return render(request, 'question.html', {'elems': answers, 'question': question, 'form': form})
