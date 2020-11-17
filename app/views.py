from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.models import Question, Answer
from django.template.defaulttags import register

# Create your views here.


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

question_list = [
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
