from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.models import Question, Answer
from django.template.defaulttags import register
from django.contrib import auth
from blog.forms import LoginForm, AskForm, RegisterForm
from django.contrib.auth.decorators import login_required


# Create your views here.


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



def login(request):
    if request.method =='GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                request.session['hello']= 'world'
                # доставать request.session.pop('hello')
                auth.login(request, user)
                return redirect("/") # нужен правильный редирект, обратно на страницу, откуда пришел

    ctx = {'form': form}
    return render(request, 'login.html', ctx)

def logout(request):
    auth.logout(request)
    return redirect("/")

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.nickname = form.cleaned_data.get('nickname')
            user.profile.avatar = form.cleaned_data.get('avatar')
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
            return redirect(reverse('question', kwargs={'question_id': question.pk}))
    ctx = {'form': form}
    return render(request, 'ask.html', ctx)

def question(request):
    return render(request, 'question.html', {})

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

    from pprint import pformat
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
    return render(request, 'index.html', {'questions': questions, 'nums': nums})

def settings(request):
    return render(request, 'settings.html', {})

def question(request, question_id):
    question = Question.objects.find_id(question_id)
    answers = Answer.objects.find_by_q(question_id)
    paginator = Paginator(answers, 2) # Show 2
    page = request.GET.get('page', 1)
    answers = paginator.get_page(page)
    return render(request, 'question.html', {'answers': answers, 'question': question})
