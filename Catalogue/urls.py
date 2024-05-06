from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import advanced_search, authors_list
from .views import author_detail
from .views import search

urlpatterns = [
    path("books/", views.books, name="books"),
    path("book_detail/<uuid:book_id>/", views.book_detail, name="book_detail"),
    
    ############################ Authors ##############################
    path("authors/", views.authors, name="authors"),
    path("authors/<uuid:author_id>/", views.author_detail, name="author_detail"),
    
    #   Url des commentaires et des réponses
    path("comment/<uuid:comment_id>/reply/", views.reply_to_comment, name="reply"),
    path("answer/<uuid:answer_id>/edit/", views.edit_answer, name="edit_answer"),
    path("answer/<uuid:answer_id>/delete/", views.delete_answer, name="delete_answer"),
    # url pour editer ou supprimer un commentaires
    path("comment/<uuid:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path(
        "comment/<uuid:comment_id>/delete/", views.delete_comment, name="delete_comment"
    ),
    path('ma_vue/<int:page>', views.my_books, name='ma_vue_pagine'),
    path('ma_vue/', views.my_books, name='ma_vue'),
    path('books/search', search, name='search'),
    path('books/advanced_search', advanced_search, name='advanced_search'),

    path('books/add_to_cart/<str:bookId>', views.add_to_cart, name="add_to_cart"),
    path('cart', views.get_cart_books, name="get_cart_books"),
    path('remove_from_cart/<str:bookId>', views.remove_from_cart, name="remove_from_cart"),
    path('checkout', views.checkout, name="checkout"),
    
    # url pour la section des livres les plus recommenders
    path('recommended', views.books_by_recommended, name="recommendeds"),
    
]
