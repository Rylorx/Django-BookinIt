from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from users.models import UserBook
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def books_view(request):
    books = Book.objects.all()
    context = {"books": books, 
               
               "pma_flag": (
                request.user.groups.filter(name="PMA").exists()
                if request.user.is_authenticated
                else False
                ),
               }
    return render(request, "books/books_view.html", context)

@login_required
def add_to_shelf(request, book_id, status):
    book = get_object_or_404(Book, id=book_id)
    userbook, created = UserBook.objects.get_or_create(user=request.user, book=book, status=status)
    if created:
        messages.success(request, f"'{book.title}' added to your {status.replace('_', ' ').title()} shelf.")
    else:
        messages.info(request, f"'{book.title}' is already in your {status.replace('_', ' ').title()} shelf.")
    return redirect('books_view')

@login_required
def remove_from_shelf(request, book_id, status):
    book = get_object_or_404(Book, id=book_id)
    userbook = get_object_or_404(UserBook, user=request.user, book=book, status=status)
    userbook.delete()
    messages.success(request, f"'{book.title}' removed from your {status.replace('_', ' ').title()} shelf.")
    return redirect('user_profile')
