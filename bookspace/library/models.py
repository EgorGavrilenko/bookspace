from django.db import models, IntegrityError, transaction


class Book(models.Model):
    class Meta:
        unique_together = (('title', 'author'),)

    title = models.CharField(max_length=120)
    author = models.CharField(max_length=50)

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
    def get_book(author, title):
        try:
            book = Book.objects.get(title=title, author=author)
        except Book.DoesNotExist:
            book = None
        return book


class User(models.Model):
    class Meta:
        unique_together = (('name'),)

    name = models.CharField(max_length=50)
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
    def get_all_users():
        users = User.objects.all()
        userslist = []
        for user in users:
            userslist.append(user.name)
        data = {'users': userslist}
        return data

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
    userDescription = models.TextField()

    def __str__(self):
        return "User: {}; Book: {}; description: {}".format(self.userID, self.bookID, self.userDescription)

    @staticmethod
    def get_user_books(name):
        user = User.objects.get(name=name)
        try:
            userBooks = UserAndBook.objects.filter(userID=user)

            userBooksDict = {}
            userBooksDict["name"] = name
            userBooksDict["books"] = []
            for userBook in userBooks:
                userBooksDict["books"].append({"author": userBook.bookID.author, "title": userBook.bookID.title,
                                               "description": userBook.userDescription})

            return userBooksDict
        except UserAndBook.DoesNotExist:
            return None

    def assign_book_for_user(self, title, author, name):
        book = Book.get_book_or_create(author=author, title=title)
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
    def edit_description_of_book(name, author, title, description):
        user = User.get_user(name=name)
        book = Book.get_book(author=author, title=title)
        userAndBook = UserAndBook.objects.get(userID=user, bookID=book)
        userAndBook.userDescription = description
        userAndBook.save()
