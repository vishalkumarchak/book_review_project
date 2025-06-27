from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from unittest.mock import patch
from .models import Book
from rest_framework.test import APIClient

class BookTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Test Book", author="Tester")
        self.client_api = APIClient()

    def test_create_book_model(self):
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(str(self.book), "Test Book")

    def test_get_books_view(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_cache_miss_then_hit(self):
        cache.delete("books")
        with self.assertNumQueries(1):
            self.client.get(reverse("book_list"))  
        with self.assertNumQueries(0):
            self.client.get(reverse("book_list"))  

    @patch("django.core.cache.cache.get", side_effect=Exception("Redis Down"))
    def test_fallback_when_cache_fails(self, mock_cache):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_api_books_view(self):
        response = self.client_api.get("/api/books/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], "Test Book")
