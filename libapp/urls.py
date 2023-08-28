from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('explore', explore_view, name='explore_view'),
    path('book_request/', book_request_view, name='book_request'),
    path('get_subjects/', get_subjects_view, name='get_subjects'),
    path('get_books/', get_books_view, name='get_books'),
    path('book_request/', book_request_view, name='book_request'),
    path('login',login,name="login"),
    path('register',register,name="register"),
    path('signup',signup,name="signup"),
    path('login_user',login_user,name="login"),
    path('logout/', logout, name='logout'),
    path('dashboard', user_dashboard_view, name='user_dashboard'),
    path('return_book/', return_book_view, name='return_book'),
    path('explore/', explore, name='explore'),
    path('aboutus', aboutus_view, name='aboutus_view'),
    path('login_librarian', login_librarian, name='login_librarian'),
    path('update_book_details/<int:book_pk>/', update_book_details, name='update_book_details'),
    path('save_book_details/<int:book_pk>/', save_book_details, name='save_book_details'),
    path('add_book', render_add_new_book_page, name='add_new_book'),
    path('save_book', save_new_book, name='save_new_book'),
    path('ldashboard', librarian_dashboard, name='librarian_dashboard'),
    path('remind_user/', remind_user, name='remind_user'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)