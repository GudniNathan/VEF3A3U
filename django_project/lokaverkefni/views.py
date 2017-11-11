from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .forms import LoginForm
from datetime import date
from . import validateKennitala

from .models import Courses
from django.db import connection

# Create your views here.
def index(request):
    path = 'lokaverkefni/index.html'
    yes = "nodata"
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if validateKennitala.validate(form.cleaned_data['login_username']):
                yes = "VALID"
            else: yes = "INVALID"
            yes = form

    context = {
        "year":date.today().year,
        "postData": yes,
    }
    return render(request, path, context)

def chart(request):
    path = 'lokaverkefni/chart.html'
    courses = Courses.objects.all()
    context = {
        "year": date.today().year,
        "data": courses,
    }
    return render(request, path, context)

def nextSemester(request):
    path = 'lokaverkefni/index.html'
    context = {
        "year": date.today().year,
    }
    return render(request, path, context)
