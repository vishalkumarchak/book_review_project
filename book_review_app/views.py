from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache
from django.http import HttpResponseServerError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Review
from .serializers import BookSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def api_books(request):
    try:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"API error: {e}")
        return Response({"error": "Unable to fetch books"}, status=500)

def book_list(request):
    try:
        books = cache.get("books")
        if not books:
            books = list(Book.objects.all())
            try:
                cache.set("books", books, timeout=60)
            except Exception as ce:
                logger.warning(f"Redis cache set failed: {ce}")
    except Exception as e:
        logger.error(f"Redis cache get failed: {e}")
        books = list(Book.objects.all())

    try:
        return render(request, "books.html", {"books": books})
    except Exception as te:
        logger.error(f"Template error: {te}")
        return HttpResponseServerError("Internal server error.")

def add_book(request):
    if request.method == "POST":
        try:
            title = request.POST["title"]
            author = request.POST["author"]
            cover_image = request.FILES.get("cover_image")
            Book.objects.create(title=title, author=author, cover_image=cover_image)
            try:
                cache.delete("books")
            except Exception as ce:
                logger.warning(f"Failed to delete Redis cache: {ce}")
            return redirect("book_list")
        except Exception as e:
            logger.error(f"Book creation failed: {e}")
            return HttpResponseServerError("Error adding book.")
    return render(request, "add_book.html")

def book_reviews(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)
        return render(request, "reviews.html", {"book": book, "reviews": book.reviews.all()})
    except Exception as e:
        logger.error(f"Review load failed: {e}")
        return HttpResponseServerError("Unable to load reviews.")

def add_review(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)
        if request.method == "POST":
            content = request.POST["content"]
            rating = request.POST["rating"]
            review_image = request.FILES.get("review_image")
            Review.objects.create(book=book, content=content, rating=rating, review_image=review_image)
            return redirect("book_reviews", book_id=book.id)
        return render(request, "add_review.html", {"book": book})
    except Exception as e:
        logger.error(f"Review submission failed: {e}")
        return HttpResponseServerError("Error adding review.")



def delete_book(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)
        book.delete()

        try:
            cache.delete("books") 
        except Exception as ce:
            logger.warning(f"Failed to clear cache after delete: {ce}")

        return redirect("book_list")
    except Exception as e:
        logger.error(f"Book deletion failed: {e}")
        return HttpResponseServerError("Error deleting book.")
