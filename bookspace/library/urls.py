from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import add_user, assign_book, get_books, home, edit_description, delete_user, delete_book, edit_user


urlpatterns = [
    path('api/addUser', add_user),
    path('api/editDescription', edit_description),
    path('api/assignBook', assign_book),
    path('api/getBooks', get_books),
    path('api/delete', delete_user),
    path('api/editUser', edit_user),
    path('api/deleteBook', delete_book),
    path('<int:page_number>/', home),
    path('', home),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)