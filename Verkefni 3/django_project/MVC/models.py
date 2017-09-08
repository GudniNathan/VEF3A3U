from django.db import models

# Create your models here.
class Book(models.Model):
    book_title = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    book_publisher = models.CharField(max_length=255)
    book_year = models.PositiveIntegerField()

    def __str__(self):
        return self.book_title +  ' by ' + self.book_author