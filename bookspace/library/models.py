import datetime
from django.db.models import Sum, Count
from django.db import models, IntegrityError, transaction


class Book(models.Model):
    class Meta:
        unique_together = (('title', 'author', 'price','number_of_pages'),)

    title = models.CharField(max_length=120)
    author = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)
    number_of_pages = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'author: {} title: {}'.format(self.author, self.title)

    def add_new_book(self):
        try:
            with transaction.atomic():
                super().save()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def get_book_or_create(author, title):
        try:
            book = Book.objects.get(title=title, author=author)
        except Book.DoesNotExist:
            book = Book(title=title, author=author)
            book.add_new_book()
        return book

    @staticmethod
    def get_book(author, title, price, number_of_pages):
        try:
            book = Book.objects.get(title=title, author=author, price=price, number_of_pages=number_of_pages)
        except Book.DoesNotExist:
            book = None
        return book


class User(models.Model):
    class Meta:
        unique_together = (('name'),)

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to = 'user_image', default='media/default.png')
    books = models.ManyToManyField(Book, null=True, blank=True, through="UserAndBook")

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
        except Book.DoesNotExist:
            return False
        user.delete()
        return True

    @staticmethod
    def get_all_users():
        users = User.objects.all()
        return users

    @staticmethod
    def get_user(name):
        try:
            user = User.objects.get(name=name)
        except Book.DoesNotExist:
            user = None
        return user



class UserAndBook(models.Model):
    class Meta:
        unique_together = (('userID', 'bookID'),)
        verbose_name = "User and Book"
        verbose_name_plural = "Users and Books"

    userID = models.ForeignKey(User, on_delete=models.PROTECT)
    bookID = models.ForeignKey(Book, on_delete=models.PROTECT)
    description = models.TextField(default="")
    data_of_creation = models.DateField(default=datetime.date.today)
    data_of_change = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "User: {}; Book: {}; description: {}".format(self.userID, self.bookID, self.description)

    @staticmethod
    def get_user_books(name):
        user = User.objects.get(name=name)
        try:
            userBooks = UserAndBook.objects.filter(userID=user)

            userBooksDict = {}
            userBooksDict["user"] = user
            userBooksDict["books"] = []
            for userBook in userBooks:
                userBooksDict["books"].append({"author": userBook.bookID.author,
                                               "title": userBook.bookID.title,
                                               "number_of_pages": userBook.bookID.number_of_pages,
                                               "price": userBook.bookID.price,
                                               "description": userBook.description,
                                               "data_of_creation": userBook.data_of_creation,
                                               "data_of_change": userBook.data_of_change}
                                              )

            return userBooksDict
        except UserAndBook.DoesNotExist:
            return None

    def assign_book_for_user(self, book, name):
        user = User.objects.get(name=name)
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
        user = User.objects.get(name=name)
        countBook = User.objects.get(name=name).books.count()
        sumPrice = User.objects.annotate(total=Sum('books__price')).get(name=name)
        if countBook == 0:
            return 0
        else:
            return sumPrice.total/countBook

    @staticmethod
    def edit_description_of_book(name, author, title, price, number_of_pages, description):
        user = User.get_user(name=name)
        book = Book.get_book(author=author, title=title, price=price, number_of_pages=number_of_pages)
        userAndBook = UserAndBook.objects.get(userID=user, bookID=book)
        userAndBook.description = description
        userAndBook.data_of_change = datetime.date.today()
        userAndBook.save()
