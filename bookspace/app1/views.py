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

from .models import (add_new_user, get_all_users, add_new_book, assign_book_for_user,
                     get_user_books, get_user_books, edit_description_of_book)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def add_user(request):
    name = request.data.get("name")
    if name is None:
        return Response({'error': 'Please provide name'},
                        status=HTTP_400_BAD_REQUEST)
    if add_new_user(name):
        return Response(status=HTTP_200_OK)
    else:
        return Response({'error': 'Such name exists'},
                        status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def add_book(request):
    title = request.data.get("title")
    author = request.data.get("author")
    if title is None or author is None:
        return Response({'error': 'Please provide both title and author'},
                        status=HTTP_400_BAD_REQUEST)
    add_new_book(title, author)
    return Response({"status": "success"}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def assign_book(request):
    title = request.data.get("title")
    author = request.data.get("author")
    name = request.data.get("name")
    description = request.data.get("description")
    if title is None or author is None or name is None or description is None:
        return Response({'error': 'Please provide both title and author'},
                        status=HTTP_400_BAD_REQUEST)

    if assign_book_for_user(title=title, author=author,
                            name=name, description=description):
        return Response(status=HTTP_200_OK)
    else:
        return Response({'error': 'Such book exists'},
                        status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["GET"])
@renderer_classes((TemplateHTMLRenderer,))
@permission_classes((AllowAny,))
def get_books(request):
    name = request.query_params.get('name')
    if name is None:
        return Response({'error': 'Please provide name'},
                        status=HTTP_400_BAD_REQUEST)
    data = get_user_books(name)
    return Response(data, template_name='books.html')


@csrf_exempt
@api_view(["POST", "GET"])
@renderer_classes((TemplateHTMLRenderer,))
@permission_classes((AllowAny,))
def home(request):
    data = {'users': get_all_users()}
    return Response(data, template_name='users.html')


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def edit_description(request):
    title = request.data.get("title")
    author = request.data.get("author")
    name = request.data.get("name")
    description = request.data.get("description")
    if title is None or author is None or name is None or description is None:
        return Response({'error': 'Please provide both title and author'},
                        status=HTTP_400_BAD_REQUEST)
    edit_description_of_book(title=title, author=author,
                             name=name, description=description)
    return Response({"status": "success"}, status=HTTP_200_OK)
