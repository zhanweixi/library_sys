# -*-conding:UTF-8-*-
from apps.library.views import LibraryView, BorrowView
from django.urls import path

urlpatterns = [
    path('books', LibraryView.as_view(), name='books'),
    path('borrow', BorrowView.as_view(), name='borrow'),
]
