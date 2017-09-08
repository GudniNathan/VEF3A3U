from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    page = loader.get_template('routing/index.html')
    return HttpResponse(page.render(request))

def jobs(request):
    page = loader.get_template('routing/jobs.html')
    return HttpResponse(page.render(request))

def bio(request):
    page = loader.get_template('routing/bio.html')
    return HttpResponse(page.render(request))

def pics(request):
    page = loader.get_template('routing/pics.html')
    return HttpResponse(page.render(request))