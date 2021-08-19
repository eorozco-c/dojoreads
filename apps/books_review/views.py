from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import User, Author, Book, UserBook
import bcrypt
# Create your views here.
def index(request):
    if request.method == "GET":
        if "id" in request.session:
            return redirect("/books")
    return render(request, "index.html")

def create_user(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password_hs = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        errors = User.objects.validator_reg(request.POST)
        if len(errors) > 0:
            return JsonResponse(errors)
        usuario = User.objects.create(first_name=fname,last_name=lname,email=email,password=password_hs)
        request.session["id"] = usuario.id
        return JsonResponse({"resultado": usuario.id })
    return redirect("/")

def login(request):
    if request.method == "POST":
        email = request.POST["email_login"]
        password = request.POST["password_login"]
        errors = User.objects.validator_log(request.POST)
        if len(errors) > 0:
            return JsonResponse(errors)   
        try:
            usuario = User.objects.get(email=email)
        except:
            errors = {
                "email_login" : "Email no existe favor registrese"
            }
            return JsonResponse(errors) 
        if bcrypt.checkpw(password.encode(), usuario.password.encode()):
            request.session["id"] = usuario.id
            return JsonResponse({"resultado": usuario.id })
        else:
            errors = {
                "password_login" : "Contraseña incorrecta"
            }
            return JsonResponse(errors)

def logout(request):
    if request.method == "GET":
        if "id" in request.session:
            del request.session['id']
        return redirect("/")

def books(request):
    if request.method == "GET":
        if "id" in request.session:
            idusuario = request.session["id"]
            context = {
                "usuario" : User.objects.get(id=idusuario),
                "libros" : Book.objects.all().order_by("-id"),
            }
            return render(request, "books.html", context)
    return redirect("/")

def create_book(request):
    if request.method == "GET":
        if "id" in request.session:
            idusuario = request.session["id"]
            context = {
                "usuario" : User.objects.get(id=idusuario),
                "autores" : Author.objects.all(),
                "reviews" : UserBook.objects.all(),
            }
            return render(request, "new_book.html", context)
        return redirect("/")
    elif request.method == "POST":
        if "id" in request.session:
            errors = Book.objects.validate(request.POST)
            if len(errors) > 0:
                return JsonResponse(errors)
            title = request.POST["book_title"]
            authorName = request.POST["author_list"].split()
            if request.POST["author_list"] == "":
                authorName = request.POST["add_author"].split()
                author = Author.objects.create(first_name=authorName[0], last_name=authorName[1])
            author = Author.objects.get(first_name__iexact=authorName[0], last_name__iexact=authorName[1])
            uploaded_by = User.objects.get(id=request.session["id"])
            new_book = Book.objects.create(title=title,author=author,uploaded_by=uploaded_by)
            UserBook.objects.create(user=uploaded_by,book=new_book,rating=request.POST["rating"],review=request.POST["review"])
            return JsonResponse({"resultado" : 200})
        return redirect("/")
        
def view_book(request,idBook):
    if request.method == "GET":
        if "id" in request.session:
            idusuario = request.session["id"]
            context = {
                "usuario" : User.objects.get(id=idusuario),
                "libro" : Book.objects.get(id=idBook),
                "reviews" : UserBook.objects.filter(book=Book.objects.get(id=idBook)),
            }
            return render(request, "view_book.html", context)
        return redirect("/")
    elif request.method == "POST":
        if "id" in request.session:
            print(request.POST)
            errors = UserBook.objects.validate_review(request.POST)
            if len(errors) > 0:
                 return JsonResponse(errors)
            uploaded_by = User.objects.get(id=request.session["id"])
            book = Book.objects.get(id=idBook)
            new_review = UserBook.objects.create(user=uploaded_by,book=book,rating=request.POST["addRating"],review=request.POST["addReview"])
            data = {
                "resultado" : idBook,
                "reviewid" : new_review.id,
            }
            return JsonResponse(data)
        return redirect(f"/books/{idBook}")
    return redirect("/")

def view_user(request,idUser):
    if request.method == "GET":
        if "id" in request.session:
            idusuario = request.session["id"]
            context = {
                "usuario" : User.objects.get(id=idusuario),
                "reviews" : UserBook.objects.filter(user=User.objects.get(id=idUser)),
                "userReview" : User.objects.get(id=idUser),
            }
            return render(request, "view_user.html", context)
    return redirect("/")

def delete_review(request,idReview):
    if request.method == "GET":
        if "id" in request.session:
            delete_review = UserBook.objects.get(id=idReview)
            delete_review.delete()   
    return redirect("/")