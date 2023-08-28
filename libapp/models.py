from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    department = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    books = models.JSONField(default=list)
    notifications = models.JSONField(default=list)
    is_librarian = models.BooleanField(default=False)  # Add this field for Librarian identification

    def __str__(self):
        return self.username
    
    def take_book(self, book):
        start_date = timezone.now()
        end_date = start_date + timezone.timedelta(days=10)

        book_info = {
            'title': book.title,
            'image': book.image.url if book.image else None,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }

        self.books.append(book_info)
        self.save()

# Model for Librarian
class Librarian(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username
