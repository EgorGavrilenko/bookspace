import datetime
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import User, UserAndBook, Book


class UserTest(TestCase):
    def setUp(self):
        user = User.objects.create(name='U')

    def test_user(self):
        user = User.objects.get(name='U')
        name = user.name
        self.assertEquals(name, 'U')

    def test_get_user(self):
        user = User.get_user(name='U')
        name = user.name
        self.assertEquals(name, 'U')

    def test_get_all_user(self):
        response = self.client.get('/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')

    def test_add_user(self):
        response = self.client.post('/api/addUser', {'name': 'P'})
        self.assertEquals(response.status_code, 302)

    def test_edit_user(self):
        image = SimpleUploadedFile(name='2.jpg', content=open('./media/user_image/2.jpg', 'rb').read(), content_type='image/*')
        response = self.client.post('/api/editUser', {'name': 'U', 'image': image})
        self.assertEquals(response.status_code, 302)

    def test_delete_user(self):
        response = self.client.post('/api/delete', {'name': 'U'})
        self.assertEquals(response.status_code, 302)


class BookTest(TestCase):
    def setUp(self):
        book = Book.objects.create(author='A', title='T', price=100, number_of_pages=200)

    def test_book(self):
        book = Book.objects.get(author='A', title='T', price=100, number_of_pages=200)
        author = book.author
        title = book.title
        price = book.price
        number_of_pages = book.number_of_pages
        self.assertEquals(author, 'A')
        self.assertEquals(title, 'T')
        self.assertEquals(price, 100)
        self.assertEquals(number_of_pages, 200)

    def test_get_book(self):
        book = Book.get_book(author='A', title='T', price=100, number_of_pages=200)
        author = book.author
        title = book.title
        price = book.price
        number_of_pages = book.number_of_pages
        self.assertEquals(author, 'A')
        self.assertEquals(title, 'T')
        self.assertEquals(price, 100)
        self.assertEquals(number_of_pages, 200)

    def test_get_or_create_book(self):
        book = Book.get_book_or_create(author='1', title='2', price=100, number_of_pages=200)
        author = book.author
        title = book.title
        price = book.price
        number_of_pages = book.number_of_pages
        self.assertEquals(author, '1')
        self.assertEquals(title, '2')
        self.assertEquals(price, 100)
        self.assertEquals(number_of_pages, 200)


class UserAndBookTest(TestCase):
    def setUp(self):
        book = Book.objects.create(author='A1', title='T1', price=100, number_of_pages=200)
        user = User.objects.create(name='U1')
        UserAndBook.objects.create(bookID=book, userID=user, description="1")

    def test_get_user_books(self):
        user = User.objects.get(name='U1')
        name = user.name
        request = "/api/getBooks?name="+name
        response = self.client.get(request)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'books.html')

    def test_edit_description(self):
        user = User.objects.get(name='U1')
        name = user.name
        book = Book.objects.get(author='A1', title='T1', price=100, number_of_pages=200)
        author = book.author
        title = book.title
        price = book.price
        number_of_pages = book.number_of_pages
        description = '2'
        response = self.client.post('/api/editDescription',
                                    {'author': author, 'title': title,
                                     'price': price, 'number_of_pages': number_of_pages,
                                     'name': name, 'description': description})
        self.assertEquals(response.status_code, 302)
        userAndBook = UserAndBook.objects.get(userID=user, bookID=book)
        self.assertEquals(userAndBook.description, '2')

    def test_assign_book(self):
        user = User.objects.get(name='U1')
        name = user.name
        author = 'A2'
        title = 'T2'
        price = 100
        number_of_pages = 200
        description = '2'

        response = self.client.post('/api/assignBook',
                                    {'author': author, 'title': title,
                                     'price': price, 'number_of_pages': number_of_pages,
                                     'name': name, 'description': description})
        self.assertEquals(response.status_code, 302)

    def test_delete_book(self):
        user = User.objects.get(name='U1')
        name = user.name
        book = Book.objects.get(author='A1', title='T1', price=100, number_of_pages=200)
        author = book.author
        title = book.title
        price = book.price
        number_of_pages = book.number_of_pages

        response = self.client.post('/api/deleteBook',
                                    {'author': author, 'title': title,
                                     'price': price, 'number_of_pages': number_of_pages,
                                     'name': name})
        self.assertEquals(response.status_code, 302)
