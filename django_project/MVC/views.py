from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from .models import Book
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
def index(request):
    path = 'MVC/index.html'
    all_books = Book.objects.all()
    context = {
        'all_books': all_books,
    }
    return render(request, path, context)

def detail(request, book_id):
    path = 'MVC/book_info.html'
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'book': book,
        'book_id': book_id,
    }
    return render(request, path, context)
