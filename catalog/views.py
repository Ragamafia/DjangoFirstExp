from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic


def index(request):
    # Функция отображения для домашней страницы сайта (показать кол-во книг, экземпляров, авторов и т.д.
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_harry_potter = Book.objects.filter(title__contains="Гарри").count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри переменной контекста "context"
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books, 'num_instances': num_instances, 'num_instances_available': num_instances_available,
            'num_authors': num_authors, 'num_genres': num_genres, 'num_harry_potter': num_harry_potter,
            'num_visits': num_visits},
    )


class BookListView(generic.ListView):
    model = Book


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


class GenreListView(generic.ListView):
    model = Genre


class GenreDetailView(generic.DetailView):
    model = Genre
