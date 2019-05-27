from django.contrib import admin
from django.urls import path
from .views import add_user, add_book, assign_book, get_books, home, edit_description


urlpatterns = [
    path('api/addUser', add_user),
    path('api/addBook', add_book),
    path('api/editDescription', edit_description),
    path('api/assignBook', assign_book),
    path('api/getBooks', get_books),
    path('', home),
    path('admin/', admin.site.urls)
]
