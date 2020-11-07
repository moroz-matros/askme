from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.models import Article

# Create your views here.

question_list = [
	{
		'id': idx,
		'title': f'title{idx}',
		'text': 'text text',
	} for idx in range(10)
]

answer_list = [
    {
        'id': idx,
        'title': f'title{idx}',
        'text': 'text text',
    } for idx in range(10)
]


def login(request):
    return render(request, 'login.html', {})

def signup(request):
    return render(request, 'signup.html', {})

def ask(request):
    return render(request, 'ask.html', {})

def question(request):
    return render(request, 'question.html', {})

def hot(request):
    paginator = Paginator(question_list, 5) # Show 5 
    page = request.GET.get('page', 1)
    questions = paginator.get_page(page)
    return render(request, 'hot.html', {'questions': questions})

def tag(request, tag):
    return render(request, 'tag.html', {'tag': tag})

def listing(request):
    questions = Article.objects.all()
    paginator = Paginator(questions, 2) # Show 2
    page = request.GET.get('page', 1)
    questions = paginator.get_page(page)

    return render(request, 'index.html', {'questions': questions})

def settings(request):
    return render(request, 'settings.html', {})

def question(request):
    paginator = Paginator(answer_list, 2) # Show 5 
    page = request.GET.get('page', 1)
    answers = paginator.get_page(page)
    return render(request, 'question.html', {'answers': answers})
