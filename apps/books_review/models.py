from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETTER_REGEX = re.compile(r'^[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def validator_reg(self,postData):
        errores = {}
        if not LETTER_REGEX.match(postData["fname"]) or len(postData['fname']) < 2:
            errores['fname'] = "El nombre debe contener solo letras y tener un minimo de 2 caracteres"
        if not LETTER_REGEX.match(postData["lname"]) or len(postData['lname']) < 2:
            errores['lname'] = "El apellido debe contener solo letras y tener un minimo de 2 caracteres"
        if not EMAIL_REGEX.match(postData['email']):     
            errores['email'] = "Email invalido"
        if len(postData["password"]) < 8:
            errores['password'] = "Contraseña debe tener minimo 8 caracteres"
        if postData["password"] != postData["confirm_password"]:
            errores["confirm_password"] = "Contraseña no coincide"
        if self.filter(email__iexact=postData["email"]).exists():
            errores["email"] = "Email ya existe, favor ingresar uno nuevo"
        return errores
    def validator_log(self,postData):
        errores = {}
        if not EMAIL_REGEX.match(postData['email_login']):     
            errores['email_login'] = "Email invalido"
        if len(postData["password_login"]) < 8:
            errores['password_login'] = "Contraseña debe tener minimo 8 caracteres"
        return errores

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class AuthorManager(models.Manager):
    def validate_author(self,postData):
        errors = {}
        if not LETTER_REGEX.match(postData["add_author"]) or len(postData['add_author']) < 2:
            errors['add_author'] = "El nombre debe contener un minimo de 2 caracteres y debe contener solo letras"
        return errors

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()

class BookManager(models.Manager):
    def validate(self,postData):
        errors = {}
        authorName = postData["add_author"].split()
        if postData["book_title"] == "":
            errors['book_title'] = "Título está vacío"
        if postData["add_author"] == "" and postData["author_list"] == "":
            errors['author_list'] = "Debe ingresar un autor"
        for nombre in authorName:
            if not LETTER_REGEX.match(nombre):
                errors['add_author'] = "El nombre debe contener solo letras"
        if len(authorName) >= 2 and self.filter(author__first_name__iexact=authorName[0],author__last_name__iexact=authorName[1]).exists():
            errors['add_author'] = "Autor ya existe"
        if len(authorName) > 0 and len(authorName) < 2:
            errors['add_author'] = "El nombre del autor debe contener Nombre y Apellido"
        if len(postData["review"]) < 5:
            errors['review'] = "review debe tener mas de 5 caracteres"
        if int(postData["rating"]) < 1 or int(postData["rating"]) > 5 :
            errors['rating'] = "Rating debe ser de 1 a 5"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class  UserBookManager(models.Manager):
    def validate_review(self,postData):
        errors = {}
        if int(postData["addRating"]) < 1 or int(postData["addRating"]) > 5 :
            errors['addRating'] = "Rating debe ser de 1 a 5"
        if len(postData["addReview"]) < 5:
            errors['addReview'] = "review debe ser de 5 caracteres minimo"
        return errors

class UserBook(models.Model):
    user = models.ForeignKey(User,related_name="review_user", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="review_book",on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserBookManager()