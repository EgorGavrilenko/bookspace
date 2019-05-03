from django.test import TestCase, SimpleTestCase

from .models import (User, UserAndBook, Book, add_new_user,
                     get_all_users, add_new_book, assign_book_for_user,
                     get_user_books, get_user_books, edit_description_of_book)


class MyTest(TestCase):

    @classmethod
    def setUp(cls):
        book = Book.objects.create(author='A', title='T')
        user = User.objects.create(name='U')
        UserAndBook.objects.create(
            bookID=book, userID=user, userDescription="1")

    def test_user(self):
        user = User.objects.get(name='U')
        name = user.name
        self.assertEquals(name, 'U')

    def test_book(self):
        book = Book.objects.get(author='A', title='T')
        author = book.author
        title = book.title
        self.assertEquals(author, 'A')
        self.assertEquals(title, 'T')

    def test_get_all_user(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')

    def test_post_get_user_books(self):
        user = User.objects.get(name='U')
        name = user.name
        request = "/api/getBooks?name="+name
        response = self.client.get(request)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'books.html')

    def test_post_edit_description(self):
        user = User.objects.get(name='U')
        name = user.name
        book = Book.objects.get(author='A', title='T')
        author = book.author
        title = book.title
        description = '2'
        response = self.client.post('/api/editDescription',
                                    {'author': author, 'title': title,
                                     'name': name, 'description': description})
        self.assertEquals(response.status_code, 200)
        userAndBook = UserAndBook.objects.get(userID=user, bookID=book)
        self.assertEquals(userAndBook.userDescription, '2')

    def test_add_user(self):
        user = User.objects.get(name='U')
        name = user.name
        response = self.client.post('/api/addUser', {'name': name})
        self.assertEquals(response.status_code, 400)

        response = self.client.post('/api/addUser', {'name': 'P'})
        self.assertEquals(response.status_code, 200)

    def test_assing_book(self):
        user = User.objects.get(name='U')
        name = user.name
        book = Book.objects.get(author='A', title='T')
        author = book.author
        title = book.title
        description = '2'
        response = self.client.post('/api/assignBook',
                                    {'author': author, 'title': title,
                                     'name': name, 'description': description})
        self.assertEquals(response.status_code, 400)

        response = self.client.post('/api/assignBook',
                                    {'author': author, 'title': '11',
                                     'name': name, 'description': description})
        self.assertEquals(response.status_code, 200)
