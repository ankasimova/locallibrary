from django.db.models import Count
from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_visits': num_visits},  # num_visits appended
    )


class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        books = Book.objects.filter(author=author).annotate(num_instances=Count('bookinstance'))
        context['book_list'] = books
        return context