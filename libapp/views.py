from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Book
from .forms import BookRequestForm
from .forms import BookFilterForm
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse


# Create your views here.

def index(request):
    return render(request, 'libapp/index.html')

def home(request):
    return render(request, 'libapp/home.html')

def explore(request):
    search_query = request.GET.get('q')
    books = Book.objects.all()

    if search_query:
        # Filter the books based on the search query using Q object and icontains lookup
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query) | 
            Q(department__icontains=search_query) | 
            Q(subject__icontains=search_query)
        )

    context = {
        'books': books,
    }
    return render(request, 'libapp/explore.html', context)

def explore_view(request):
    form = BookFilterForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        department = form.cleaned_data['department']
        subjects = form.cleaned_data['subjects']

        if department:
            books = books.filter(department=department)

        if subjects:
            books = books.filter(subject__in=subjects)

    return render(request, 'libapp/explore.html', {'books': books, 'form': form})

@login_required(login_url='login')
def book_request_view(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            messages.error(request, 'Book not found.')
            return redirect('explore')

        if book.quantity > 0:
            # Reduce the book quantity by 1
            book.quantity -= 1
            book.save()

            # Add book details to the user's "books" list
            if request.user.is_authenticated:
                request.user.take_book(book)
                messages.success(request, f'Successfully taken {book.title}.')
            else:
                messages.error(request, 'You need to be logged in to take a book.')
        else:
            messages.error(request, 'The book is not available.')

    return redirect('user_dashboard')


def get_subjects_view(request):
    selected_department = request.GET.get('dept')
    subjects = Book.objects.filter(department=selected_department).values_list('subject', flat=True).distinct()
    selected_subjects = request.GET.getlist('subjects[]')
    return JsonResponse({'subjects': list(subjects), 'selected_subjects': selected_subjects})

def get_books_view(request):
    selected_department = request.GET.get('dept')
    selected_subjects = request.GET.getlist('subjects[]')
    books = Book.objects.all()
    if selected_department:
        books = books.filter(department=selected_department)
    if selected_subjects:
        books = books.filter(subject__in=selected_subjects)
    book_data = [{'title': book.title, 'description': book.description, 'author': book.author,
                  'quantity': book.quantity, 'department': book.department, 'subject': book.subject,
                  'image': book.image.url if book.image else ''} for book in books]
    return JsonResponse({'books': book_data})


def login(request):
    return render(request,'libapp/login.html')
def signup(request):
    return render(request,'libapp/register.html')
def register(request):
    print("hi")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            if len(username) < 5:
                messages.error(request,'Username must be at least 5 characters long.')
                return redirect('signup')
        
        # Check password conditions
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return redirect('signup')
            if len(phone)<10:
                messages.error(request,"Phone number should have exactly ten digits.")
                return redirect('signup')

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.save()
            redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'libapp/login.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        print("h21")
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if len(username) < 5:
                messages.error(request,'Username must be at least 5 characters long.')
                return redirect('login')
        
        # Check password conditions
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return redirect('login')
            user = authenticate(request, username=username, password=password)
            if user is not None and not user.is_librarian:  # Check if the user is not a librarian
                auth_login(request, user)
                request.session['user_id'] = user.id
                return redirect('home')  # Replace 'home' with your desired homepage URL
            
            else:
                if user is not None and user.is_librarian:
                    messages.error(request, 'Librarians are not allowed to log in here.')
                else:
                    messages.error(request, 'Invalid credentials. Please try again.')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'libapp/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect(reverse('home'))

def is_librarian(user):
    return user.is_authenticated and user.is_librarian



def user_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    user_books = user.books  # Assuming 'books' is the JSONField containing the user's books

    for book in user_books:
        end_date_str = book.get('end_date')
        if end_date_str:
            end_date = timezone.datetime.fromisoformat(end_date_str)
            book['end_date'] = end_date
            

        # Assuming 'start_date' is a field in your 'Book' model
        start_date_str = book.get('start_date')
        if start_date_str:
            start_date = timezone.datetime.fromisoformat(start_date_str)
            book['start_date'] = start_date

    context = {
        'user': user,
        'user_books': user_books,
    }

    return render(request, 'libapp/user_dashboard.html', context)



def return_book_view(request):
    if request.method == 'POST':
        book_id = int(request.POST.get('book_id'))
        user = request.user

        try:
            book_info = user.books.pop(book_id)
            book = Book.objects.get(title=book_info['title'])
            book.quantity += 1
            book.save()
            user.save()
            messages.success(request, f'Returned {book.title}.')
        except (IndexError, Book.DoesNotExist):
            messages.error(request, 'Book not found or error in returning.')

    return redirect('user_dashboard')

def aboutus_view(request):
    return render(request, 'libapp/aboutus.html')

def login_librarian(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the librarian
        user = authenticate(request, username=username, password=password, is_librarian=True)

        if user and user.is_librarian:
            auth_login(request, user)
            # Redirect to the librarian dashboard or any other librarian-specific view
            return redirect('home')  # Replace 'librarian_dashboard' with your librarian view name

        # If authentication fails, display a warning message
        messages.warning(request, 'Invalid username or password.')
        return redirect('login_librarian')  # Redirect back to the librarian login page

    return render(request, 'libapp/librarian_login.html')
    


def update_book_details(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)

    context = {'book': book}
    return render(request, 'libapp/update_book_details.html', context)

def save_book_details(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)

    if request.method == 'POST':
        # Get the form data from the request
        title = request.POST.get('title')
        description = request.POST.get('description')
        author = request.POST.get('author')
        quantity = int(request.POST.get('quantity', 0))
        department = request.POST.get('department')
        subject = request.POST.get('subject')
        image = request.FILES.get('image')

        # Update the book details
        book.title = title
        book.description = description
        book.author = author
        book.quantity = quantity
        book.department = department
        book.subject = subject
        if image:
            book.image = image
        book.save()

        return redirect('explore')  # Replace 'explore' with the appropriate URL name for your book list view

    return redirect('libapp/update_book_details', book_pk=book.pk)


def render_add_new_book_page(request):
    return render(request, 'libapp/new_book.html')

def save_new_book(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        author = request.POST.get('author')
        quantity = request.POST.get('quantity')
        department = request.POST.get('department')
        subject = request.POST.get('subject')
        description = request.POST.get('description')

        # Create and save the new book object
        book = Book(image=image, title=title, author=author, quantity=quantity,
                    department=department, subject=subject, description=description)
        book.save()

        return redirect('explore') 

    return render(request, 'libapp/new_book.html')



@user_passes_test(is_librarian)
def librarian_dashboard(request):
    # Get all users who have taken books
    users_with_books = CustomUser.objects.filter(is_librarian=False).exclude(books=[])
    user = request.user
    for user_with_books in users_with_books:
        for book in user_with_books.books:
            end_date_str = book.get('end_date')
            if end_date_str:
                end_date = timezone.datetime.fromisoformat(end_date_str)
                book['end_date'] = end_date

            start_date_str = book.get('start_date')
            if start_date_str:
                start_date = timezone.datetime.fromisoformat(start_date_str)
                book['start_date'] = start_date

    context = {
        'users_with_books': users_with_books,
        'librarian':user,
    }

    return render(request, 'libapp/librarian_dashboard.html', context)


def remind_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = int(request.POST.get('book_id'))
        user = CustomUser.objects.get(id=user_id)
        book = user.books[book_id]

        book_title = book['title']
        end_date = book['end_date']

        notification = {
            'title': book_title,
            'end_date': end_date,
        }

        user.notifications.append(notification)
        user.save()

    return redirect('librarian_dashboard')