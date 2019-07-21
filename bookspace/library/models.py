import datetime
from django.db.models import Avg
from django.db import models, IntegrityError, transaction


class Book(models.Model):
    class Meta:
        unique_together = (('title', 'author', 'price', 'number_of_pages'),)

    title = models.CharField(max_length=120)
    author = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)
    number_of_pages = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'author: {} title: {} number of pages: {}, price: {}$ ' \
            .format(self.author, self.title, self.number_of_pages, self.price)

    def add_new_book(self):
        try:
            with transaction.atomic():
                super().save()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def get_book_or_create(author, title, number_of_pages, price):
        try:
            book = Book.objects.get(title=title, author=author, number_of_pages=number_of_pages, price=price)
        except Book.DoesNotExist:
            book = Book(title=title, author=author, number_of_pages=number_of_pages, price=price)
            book.add_new_book()
        return book

    @staticmethod
    def get_book(author, title, price, number_of_pages):
        try:
            book = Book.objects.get(title=title, author=author, price=price, number_of_pages=number_of_pages)
            return book
        except Book.DoesNotExist:
            return None


class User(models.Model):
    class Meta:
        unique_together = ('name',)

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user_image', default='user_image/default.png')
    books = models.ManyToManyField(Book, through="UserAndBook")

    def __str__(self):
        return self.name

    def add_new_user(self):
        try:
            with transaction.atomic():
                super().save()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def delete_user(name):
        try:
            user = User.objects.get(name=name)
        except User.DoesNotExist:
            return False
        try:
            with transaction.atomic():
                userBooks = UserAndBook.objects.filter(userID=user)
                books = []
                for userBook in userBooks:
                    books.append(userBook.bookID)
                user.delete()
                for book in books:
                    if not User.objects.filter(books=book).exists():
                        book.delete()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def get_all_users():
        users = User.objects.all()
        return users

    @staticmethod
    def edit_user_image(name, image):
        try:
            user = User.objects.get(name=name)
        except User.DoesNotExist:
            return False
        user.image = image
        try:
            with transaction.atomic():
                user.save()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def get_user(name):
        try:
            user = User.objects.get(name=name)
            return user
        except Book.DoesNotExist:
            return None


class UserAndBook(models.Model):
    class Meta:
        unique_together = (('userID', 'bookID'),)
        verbose_name = "User and Book"
        verbose_name_plural = "Users and Books"

    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    bookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    description = models.TextField(default="")
    data_of_creation = models.DateField(default=datetime.date.today)
    data_of_change = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "User: {}; Book: {}; description: {}".format(self.userID, self.bookID, self.description)

    @staticmethod
    def get_user_books(name):
        try:
            user = User.objects.get(name=name)
            userBooks = UserAndBook.objects.filter(userID=user)
        except (UserAndBook.DoesNotExist, User.DoesNotExist):
            return None

        userBooksDict = {"user": user, "books": []}
        for userBook in userBooks:
            userBooksDict["books"].append({"author": userBook.bookID.author,
                                           "title": userBook.bookID.title,
                                           "number_of_pages": userBook.bookID.number_of_pages,
                                           "price": userBook.bookID.price,
                                           "description": userBook.description,
                                           "data_of_creation": userBook.data_of_creation,
                                           "data_of_change": userBook.data_of_change})
        return userBooksDict

    def assign_book_for_user(self, book, name):
        try:
            user = User.objects.get(name=name)
        except User.DoesNotExist:
            return False
        try:
            self.userID = user
            self.bookID = book
            with transaction.atomic():
                super().save()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def average_price(name):
        try:
            sumPrice = User.objects.annotate(total=Avg('books__price')).get(name=name)
        except User.DoesNotExist:
            return None
        if sumPrice.total is None:
            return 0
        else:
            return sumPrice.total

    @staticmethod
    def edit_description_of_book(name, author, title, price, number_of_pages, description):
        try:
            user = User.get_user(name=name)
            book = Book.get_book(author=author, title=title, price=price, number_of_pages=number_of_pages)
            userAndBook = UserAndBook.objects.get(userID=user, bookID=book)
        except (Book.DoesNotExist, User.DoesNotExist, UserAndBook.DoesNotExist):
            return False
        userAndBook.description = description
        userAndBook.data_of_change = datetime.date.today()
        try:
            with transaction.atomic():
                userAndBook.save()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def delete_user_and_book(name, author, title, price, number_of_pages):
        try:
            user = User.get_user(name=name)
            book = Book.get_book(author=author, title=title, price=price, number_of_pages=number_of_pages)
            userAndBook = UserAndBook.objects.get(userID=user, bookID=book)
        except (Book.DoesNotExist, User.DoesNotExist, UserAndBook.DoesNotExist):
            return False
        try:
            with transaction.atomic():
                userAndBook.delete()
                if not User.objects.filter(books=book).exists():
                    book.delete()
            return True
        except IntegrityError:
            return False
