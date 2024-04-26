from django.db import models
from django.urls import reverse   # Используется для создания URL-адресов путем изменения шаблонов URL-адресов

import uuid   # Требуется для генерации уникальных номеров экземпляров книг


class Genre(models.Model):   # Модель жанра книги

    name = models.CharField(max_length=200, help_text="Введите жанр книги (например, научная фантастика, "
                                                      "документальная литература)")

    def __str__(self):   # Возвращает модель (жанр) в удобочитаемом виде
        return self.name

    def get_absolute_url(self):   # Возвращает URL-адрес для доступа к конкретному экземпляру автора
        return reverse('genre-detail', args=[str(self.id)])


class Author(models.Model):   # Модель Автора

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):   # Возвращает URL-адрес для доступа к конкретному автору
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):   # Возвращает удобочитаемый вид
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):    # Модель книги (но не конкретного экземпляра книги)

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    # Внешний ключ используется, поскольку у книги может быть только один автор, но у автора может быть несколько книг.
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги.")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international'
                                                             '.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр этой книги.")
    # ManyToManyField используется, поскольку жанр может содержать множество книг. Книги могут охватывать многие жанры.

    def __str__(self):    # Возвращает модель (заголовок) в удобочитаемом виде
        return self.title

    def get_absolute_url(self):   # Возвращает URL-адрес для доступа к определенной книге
        return reverse('book-detail', args=[str(self.id)])

    def get_books(self):
        return reverse('book-detail')

    def display_genre(self):   # Создает строку для жанра. Это необходимо для отображения жанра в администраторе.
        return ', '.join(
            [genre.name for genre in self.genre.all()[:3]
             ]
        )
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):   # Модель, представляющая конкретный экземпляр книги.

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный идентификатор этой конкретной "
                                                                          "книги во всей библиотеке.")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Обслуживается'),
        ('o', 'Выдана читателю'),
        ('a', 'Доступна'),
        ('r', 'Забронирована'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Забронировать '
                                                                                                    'наличие.')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return f'{self.id}, {self.book.title}'
