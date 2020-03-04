from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from base.models import Course, Lesson, LessonBlock


def index(request):
    courses = Course.objects.all()

    context = {
        'courses': courses
    }

    return render(request, 'base/index.html', context=context)


def auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            context = {
                'errors': [
                    _('Неправильные авторизационные данные'),
                ]
            }

            return render(request, 'base/auth.html', context=context)
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'base/auth.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password,
            last_name = last_name,
            first_name = first_name
        )

        login(request, user)

        return redirect('index')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'base/register.html')


def logout(request):
    django_logout(request)
    return redirect('auth')


def learn(request, course_id):
    course = Course.objects.get(id=course_id)
    lesson_blocks = LessonBlock.objects.filter(course=course)

    context = {
        'course': course,
        'lesson_blocks': lesson_blocks
    }

    return render(request, 'base/learn.html', context=context)


def lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    context = {
        'lesson': lesson
    }

    return render(request, 'base/lesson.html', context=context)