from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .forms import LoginForm, RegisterForm
from datetime import date
from . import validateKennitala

from .models import Courses
from django.db import connections

# Create your views here.
def index(request):
    path = 'lokaverkefni/index.html'
    yes = "nodata"
    loginformErrors, registerformErrors = None, None

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if "sendlogin" in request.POST:

            loginform = LoginForm(request.POST)

        # check whether it's valid:
            if loginform.is_valid():
                #render different page if login is good
                if validateKennitala.validate(loginform.cleaned_data['login_username']):
                    yes = "VALID"
                else: yes = "INVALID"
                #yes = form
            else:
                loginformErrors = loginform.errors.as_data()

        if "sendregister" in request.POST:
            registerform = RegisterForm(request.POST)

            if registerform.is_valid():
                #render different page if login is good
                if validateKennitala.validate(registerform.cleaned_data['register_username']):
                    yes = "VALID"
                else:
                    yes = "INVALID"
            else:
                registerformErrors = registerform.errors.as_data()

    context = {
        "year":date.today().year,
        "postData": yes,
        'current_path': request.get_full_path(),
        'loginError': loginformErrors,
        'registerError': registerformErrors,
    }
    return render(request, path, context)

def chart(request):
    path = 'lokaverkefni/chart.html'
    with connections['mysql'].cursor() as cursor:
        cursor.execute("SELECT courseJSON()")
        row = cursor.fetchone()
    context = {
        "year": date.today().year,
        "data": u"%s" % (row[0]),
        'current_path': request.get_full_path(),
    }
    return render(request, path, context)

def nextSemester(request):
    path = 'lokaverkefni/nextSemester.html'
    context = {
        "year": date.today().year,
        'current_path': request.get_full_path(),
    }
    return render(request, path, context)
