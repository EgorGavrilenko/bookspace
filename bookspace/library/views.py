from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
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


# function for processing a request to add new user
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def add_user(request):
    name = request.data.get("name")
    if name is None or not name:
        return Response({'error': 'Please provide name'},
                        status=HTTP_400_BAD_REQUEST)

    user = User(name=name)

    if user.add_new_user():
        return Response(status=HTTP_200_OK)
    else:
        return Response({'error': 'Such name exists'},
                        status=HTTP_400_BAD_REQUEST)


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
    title = request.data.get("title")
    author = request.data.get("author")
    name = request.data.get("name")
    description = request.data.get("description")

    if title is None or author is None or name is None or description is None or not \
            title or not author or not name or not description:
        return Response({'error': 'Please provide both title and author'},
                        status=HTTP_400_BAD_REQUEST)


    userAndBook = UserAndBook(userDescription=description)

    if userAndBook.assign_book_for_user(title=title, author=author, name=name):
        return Response(status=HTTP_200_OK)
    else:
        return Response({'error': 'Such book exists'},
                        status=HTTP_400_BAD_REQUEST)


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
    data = UserAndBook.get_user_books(name)
    return Response(data, template_name='books.html')


# function for processing a request to get list of users in html page
@csrf_exempt
@api_view(["GET"])
@renderer_classes((TemplateHTMLRenderer,))
@permission_classes((AllowAny,))
def home(request):
    data = User.get_all_users()
    print(data)
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

    if title is None or author is None or name is None or description is None or\
            not title or not author or not name or not description:
        return Response({'error': 'Please provide both title and author'},
                        status=HTTP_400_BAD_REQUEST)

    UserAndBook.edit_description_of_book(title=title, author=author, name=name, description=description)
    return Response({"status": "success"}, status=HTTP_200_OK)
