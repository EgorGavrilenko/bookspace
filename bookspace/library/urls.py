from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from .views import add_user, add_book, assign_book, get_books, home, edit_description, delete_user


urlpatterns = [
    path('api/addUser', add_user),
    path('api/addBook', add_book),
    path('api/editDescription', edit_description),
    path('api/assignBook', assign_book),
    path('api/getBooks', get_books),
    path('api/delete', delete_user),
    path('', home),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT,}),
    ]