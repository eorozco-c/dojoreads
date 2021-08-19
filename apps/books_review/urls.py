from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.login, name="login"),
    path('logout',views.logout, name="logout"),
    path('create',views.create_user, name="createUser"),
    path('books',views.books, name="books"),
    path('createbook',views.create_book,name="createBook"),
    path('books/<int:idBook>',views.view_book,name="viewBook"),
    path('users/<int:idUser>',views.view_user,name="viewUser"),
    path('books/delete_review/<int:idReview>',views.delete_review,name="deleteReview"),
]
