from django.db import models, IntegrityError, transaction


class User(models.Model):
    class Meta:
        unique_together = (('name'),)

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    class Meta:
        unique_together = (('title', 'author'),)

    title = models.CharField(max_length=120)
    author = models.CharField(max_length=50)

    def __str__(self):
        return '{}: {}'.format(self.author, self.title)


class UserAndBook(models.Model):
    class Meta:
        unique_together = (('userID', 'bookID'),)

    userID = models.ForeignKey(User, on_delete=models.PROTECT)
    bookID = models.ForeignKey(Book, on_delete=models.PROTECT)
    userDescription = models.TextField()

    def __str__(self):
        return self.userDescription


def add_new_user(name):
    try:
        user = User(name=name)
        with transaction.atomic():
            user.save()
        return True
    except IntegrityError:
        return False


def add_new_book(title, author):
    book = Book(title=title, author=author)
    book.save()


def get_all_users():
    users = User.objects.all()
    userslist = []
    for user in users:
        userslist.append(user)
    return userslist


def assign_book_for_user(title, author, name, description):
    try:
        book = Book.objects.get(title=title, author=author)
    except Book.DoesNotExist:
        add_new_book(title=title, author=author)
        book = Book.objects.get(title=title, author=author)
    user = User.objects.get(name=name)
    try:
        userAndBook = UserAndBook(userID=user, bookID=book,
                                  userDescription=description)
        with transaction.atomic():
            userAndBook.save()
        return True
    except IntegrityError:
        return False


def get_user_books(name):
    user = User.objects.get(name=name)
    try:
        userBooks = UserAndBook.objects.select_related(
            'bookID').filter(userID=user)
        userBooksDict = {}
        userBooksDict["name"] = name
        userBooksDict["books"] = []
        for userBook in userBooks:
            userBooksDict["books"].append({"author": userBook.bookID.author, "title": userBook.bookID.title,
                                           "description": userBook.userDescription})

        return userBooksDict
    except UserAndBook.DoesNotExist:
        return None


def edit_description_of_book(name, author, title, description):
    user = User.objects.get(name=name)
    book = Book.objects.get(author=author, title=title)
    userAndBook = UserAndBook.objects.get(userID=user, bookID=book)
    userAndBook.userDescription = description
    userAndBook.save()
