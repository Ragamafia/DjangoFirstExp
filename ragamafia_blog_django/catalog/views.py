from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic


def index(request):   # Функция отображения для домашней страницы сайта

    num_books = Book.objects.all().count()   # Количество книг в библиотеке
    num_instances = BookInstance.objects.all().count()   # Всего количество экземпляров книг
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()   # Доступные книги (статус = 'a')
    num_authors = Author.objects.count()  # Количество авторов (метод all() применен по-умолчанию
    num_genres = Genre.objects.count()   # Количество авторов
    num_harry_potter = Book.objects.filter(title__contains="Гарри").count()   # Количество книг о Гарри Поттере

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # Отрисовка HTML-шаблона index.html с данными внутри переменной контекста context

    return render(
        request,
        'index.html',
        context={
            'num_books': num_books, 'num_instances': num_instances, 'num_instances_available': num_instances_available,
            'num_authors': num_authors, 'num_genres': num_genres, 'num_harry_potter': num_harry_potter,
            'num_visits':num_visits},
    )


class BookListView(generic.ListView):
    model = Book


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author



