from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Book, UserAndBook


class BookAdmin(admin.ModelAdmin):
    list_display = ["author", "title"]
    list_filter = ["author",]
    search_fields = ["author", "title"]

    class Meta:
        model = Book


class UserAndBookAdmin(admin.ModelAdmin):
    list_display = ["userID", "bookID", "description"]
    list_filter = ["userID"]

    class Meta:
        model = UserAndBook


class UserAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]

    class Meta:
        model = User


admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserAndBook, UserAndBookAdmin)
