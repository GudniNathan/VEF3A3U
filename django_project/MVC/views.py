from django.shortcuts import render
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
    try:
        # filter() will always give you a QuerySet, even if only a single object matches the query - in this case, it will be a
        #  QuerySet containing a single element.
        #  If you know there is only one object that matches your query, you can use the get() method on a Manager which
        #  returns the object directly:
        book = Book.objects.filter(id=book_id).get()
    except ObjectDoesNotExist:
        raise Http404("Book does not exist")
    context = {
        'book': book,
        'book_id': book_id,
    }
    return render(request, path, context)
