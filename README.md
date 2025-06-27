# 📚 Django Book Review App

A full-stack Django web application that allows users to view, add, and review books. This project includes Redis caching, REST API support, image uploads, exception handling, and Bootstrap-based responsive design.

---

## 🚀 Features

- ✅ Add, view, and delete books with cover images
- ✅ Add and view reviews with ratings and optional images
- ✅ Image upload and rendering using `MEDIA_ROOT`
- ✅ Redis caching for optimized book list loading
- ✅ REST API (`/api/books/`) to fetch all books
- ✅ Bootstrap 5 UI with navbar and footer
- ✅ Custom error handling and logging
- ✅ Unit tests for core functionality
- ✅ Swagger/OpenAPI integration *(optional)*

---

## 📁 Project Structure
book_review_project/
├── book_review_app/
│ ├── migrations/
│ ├── admin.py
│ ├── models.py
│ ├── serializers.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── media/
├── templates/
│ │ └── book_review/
│ │ ├── base.html
│ │ ├── books.html
│ │ ├── add_book.html
│ │ ├── reviews.html
│ │ └── add_review.html
├── book_review_project/
│ ├── settings.py
│ ├── urls.py
├── manage.py
└── README.md

