from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

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
    else:
        messages.error(request, form.errors)
    return HttpResponseRedirect('/')


# function for processing a request to edit user image
@csrf_exempt
@api_view(["POST", "FILES"])
@permission_classes((AllowAny,))
def edit_user(request):
    name = request.data.get('name')
    image = request.data.get('image')

    if name is None or image is None or not name or not image:
        messages.error(request, "data not entered")
    else:
        if not User.edit_user_image(name=name, image=image):
            messages.error(request, "data error")

    return HttpResponseRedirect('/')


# function for processing a request to delete user
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def delete_user(request):
    name = request.data.get("name")

    if name is None or not name:
        messages.error(request, "data not entered")
    else:
        if not User.delete_user(name=name):
            messages.error(request, "data error")

    return HttpResponseRedirect('/')


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
        if not userAndBook.assign_book_for_user(book=book, name=name):
            messages.error(request, "data error")

        return HttpResponseRedirect('/api/getBooks?name=' + name)
    elif form.is_bound:
        title = request.data.get("title")
        author = request.data.get("author")
        name = request.data.get("name")
        description = request.data.get("description")
        price = request.data.get("price")
        number_of_pages = request.data.get("number_of_pages")
        book = Book.get_book(author=author, title=title, number_of_pages=number_of_pages, price=price)
        userAndBook = UserAndBook(description=description)
        if not userAndBook.assign_book_for_user(book=book, name=name):
            messages.error(request, "data error")
        return HttpResponseRedirect('/api/getBooks?name=' + name)
    else:
        messages.error(request, form.errors)
        name = request.data.get("name")
        if name is None or not name:
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/api/getBooks?name=' + name)


# function for processing a request to get list of user books in html page
@api_view(["GET"])
@renderer_classes((TemplateHTMLRenderer,))
@permission_classes((AllowAny,))
def get_books(request):
    name = request.query_params.get('name')

    if name is None or not name:
        messages.error(request, "User is not found")
        return HttpResponseRedirect('/')
    else:
        data = UserAndBook.get_user_books(name=name)
        data['form'] = BookForm(initial={'name': name})
        data['average_price'] = UserAndBook.average_price(name=name)
        return Response(data, template_name='books.html')


# function for processing a request to get list of users in html page
@api_view(["GET"])
@renderer_classes((TemplateHTMLRenderer,))
@permission_classes((AllowAny,))
def home(request, page_number=1):
    users = User.get_all_users()
    form = UserForm()
    current_page = Paginator(users, 5)
    data = {'users': current_page.page(page_number), 'form': form}
    return Response(data, template_name='users.html')


# function for processing a request to delete user book
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def delete_book(request):
    title = request.data.get("title")
    author = request.data.get("author")
    name = request.data.get("name")
    price = request.data.get("price")
    number_of_pages = request.data.get("number_of_pages")

    if title is None or author is None or name is None or price is None or number_of_pages is None or \
            not title or not author or not name:
        messages.error(request, "data not entered")
        name = request.data.get("name")
        if name is None or not name:
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/api/getBooks?name=' + name)

    if not UserAndBook.delete_user_and_book(title=title, author=author, name=name,
                                            number_of_pages=number_of_pages, price=price):
        messages.error(request, "data error")

    return HttpResponseRedirect('/api/getBooks?name='+name)


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

    if title is None or author is None or name is None or price is None or number_of_pages is None or \
            not title or not author or not name:
        messages.error(request, "data not entered")
        name = request.data.get("name")
        if name is None or not name:
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/api/getBooks?name=' + name)

    if not UserAndBook.edit_description_of_book(title=title, author=author, name=name, description=description,
                                                number_of_pages=number_of_pages, price=price):
        messages.error(request, "data error")

    return HttpResponseRedirect('/api/getBooks?name='+name)
