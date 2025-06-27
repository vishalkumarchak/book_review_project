from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("api/books/", views.api_books, name="api_books"),
    path("books/add/", views.add_book, name="add_book"),
    path("books/<int:book_id>/reviews/", views.book_reviews, name="book_reviews"),
    path("books/<int:book_id>/reviews/add/", views.add_review, name="add_review"),
    path("books/<int:book_id>/delete/", views.delete_book, name="delete_book"),
]
