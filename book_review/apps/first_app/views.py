from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Author, Book, Review


def index(request):
    if 'first_name' in request.session:
        return redirect('/books')
    return render(request, "first_app/index.html")

def books(request):
    if 'first_name' in request.session:
        reviews_last_three = Review.objects.all().order_by('-id')[:3][::-1]
        other_reviews = Review.objects.all().exclude(id__in=[review.id for review in reviews_last_three])
        # this gets all the reviews except for the last three reviews

        context = {
            "reviews": reviews_last_three,
            "other_reviews": other_reviews
        }
        return render(request, "first_app/success.html", context)
    return redirect('/')

def add(request):
    if 'first_name' in request.session:
        authors = Author.objects.all()
        context = {
            'authors': authors
        }
        return render(request, "first_app/add.html", context)
    return redirect('/')

def add_book(request):
    if 'first_name' in request.session:
        review = Review.objects.validate_book(request.POST, request.session['id'])
        if review[0]:
            context = {
                "review": review[1]
            }
            return redirect('books', bid=review[1].book.id)
        else:
            for error in review[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('add')
    return redirect('/')

def book(request, bid):
    if 'first_name' in request.session:
        book = Book.objects.get(id=bid)
        reviews = Review.objects.filter(book=book)
        context = {
            "book": book,
            "reviews": reviews
        }
        # print reviews
        return render(request, "first_app/review.html", context)
    return redirect('/')

def users(request, id):
    if 'first_name' in request.session:
        user = User.objects.get(id=id)
        books = Book.objects.filter(user=user)
        reviews = Review.objects.filter(user=user)
        count = len(reviews)
        print count
        context = {
            "user": user,
            "books": books,
            "count": count,
            "reviews": reviews
        }
        return render(request, "first_app/users.html", context)
    return redirect("/")


def review(request, id, bid):
    if request.method == "POST":
        review = Review.objects.new_review(request.POST, id, bid)
        if review[0] == False:
            for error in review[1]:
                messages.add_message(request, messages.INFO, error)
        return redirect("books", bid=bid)
    return redirect("/")


def delete(request, rid, bid):
    if "first_name" in request.session:
        # book = Book.objects.get(id=bid)
        # user = User.objects.get(id=request.session['id'])
        Review.objects.review_delete(rid)
        return redirect("books", bid=bid)
    return redirect("/")


def registration(request):
    if request.method == "POST":
        result = User.objects.registration(request)
        if result[0] == False:
            for error in result[1]:
                messages.add_message(request, messages.INFO, error)
        else:
            messages.success(request, 'Registration successful')
    return redirect("/")


def login(request):
    if request.method == "POST":
        result = User.objects.login(request)
        if result[0] == False:
            for error in result[1]:
                messages.add_message(request, messages.INFO, error)
        else:
            request.session['first_name']= result[1].first_name
            request.session['id'] = result[1].id
            return redirect('/books')
    return redirect("/")


def logout(request):
    if 'first_name' in request.session:
        request.session.pop('first_name')
    return redirect('/')
