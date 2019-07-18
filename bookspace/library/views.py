from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
import urllib.parse as urlparse

from .models import User, UserAndBook, Book
from .forms import UserForm, BookForm

# function for processing a request to add new user
@csrf_exempt
@api_view(["POST", "FILES"])
@permission_classes((AllowAny,))
def add_user(request):
    form = UserForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def delete_user(request):
    user = request.data.get("id")

    if user is None or not user:
        return Response(status=HTTP_400_BAD_REQUEST)

    User.delete_user(user)
    return HttpResponseRedirect('/')

# function for processing a request to add new book
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def add_book(request):
    title = request.data.get("title")
    author = request.data.get("author")

    if title is None or author is None or not title or not author:
        return Response({'error': 'Please provide both title and author'},
                        status=HTTP_400_BAD_REQUEST)

    book = Book(title=title, author=author)
    book.add_new_book()
    if book.add_new_book():
        return Response(status=HTTP_200_OK)
    else:
        return Response({'error': 'Such name exists'},
                        status=HTTP_400_BAD_REQUEST)


# function for processing a request to assign book for user
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def assign_book(request):
    form = BookForm(request.POST)

    if form.is_valid():
        description = form.cleaned_data['description']
        name = form.cleaned_data['name']
        book = form.save()
        userAndBook = UserAndBook(description=description)
        userAndBook.assign_book_for_user(book=book, name=name)

        return HttpResponseRedirect('/api/getBooks?name='+name)


# function for processing a request to get list of user books in html page
@csrf_exempt
@api_view(["GET"])
@renderer_classes((TemplateHTMLRenderer,))
@permission_classes((AllowAny,))
def get_books(request):
    name = request.query_params.get('name')
    if name is None or not name:
        return Response({'error': 'Please provide name'},
                        status=HTTP_400_BAD_REQUEST)
    data = UserAndBook.get_user_books(name=name)
    data['form'] = BookForm(initial = {'name': name})
    data['average_price'] = UserAndBook.average_price(name=name)
    return Response(data, template_name='books.html')


# function for processing a request to get list of users in html page
@csrf_exempt
@api_view(["GET"])
@renderer_classes((TemplateHTMLRenderer,))
@permission_classes((AllowAny,))
def home(request, page_number=1):
    users = User.get_all_users()
    form = UserForm()
    current_page = Paginator(users, 5)
    data = {'users': current_page.page(page_number),'form': form}
    return Response(data, template_name='users.html')


# function for processing a request to edit book description
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def edit_description(request):
    title = request.data.get("title")
    author = request.data.get("author")
    name = request.data.get("name")
    description = request.data.get("description")
    price = request.data.get("price")
    number_of_pages = request.data.get("number_of_pages")

    if title is None or author is None or name is None or description is None or\
            not title or not author or not name or not description:
        return Response({'error': 'Please provide both title and author'},
                        status=HTTP_400_BAD_REQUEST)

    UserAndBook.edit_description_of_book(title=title, author=author, name=name, description=description,
                                         number_of_pages=number_of_pages, price=price)
    return Response({"status": "success"}, status=HTTP_200_OK)
