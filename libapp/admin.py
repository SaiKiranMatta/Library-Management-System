from django.contrib import admin
from .models import Book
from .models import CustomUser

admin.site.register(Book)
admin.site.register(CustomUser)

# Register your models here.
