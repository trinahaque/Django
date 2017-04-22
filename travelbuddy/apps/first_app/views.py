from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip


def index(request):
    if 'first_name' in request.session:
        return redirect('/success')
    return render(request, "first_app/index.html")

def success(request):
    if 'first_name' in request.session:
        user = User.objects.get(id=request.session['id'])
        user_trips = Trip.objects.filter(creator=user, joiner=user)
        # print "destination", user_trips[0].destination
        context = {
            "user_trips": user_trips
        }
        return render(request, "first_app/success.html", context)
    return redirect('/')

def add(request):
    if "first_name" in request.session:
        return render(request, "first_app/add.html")
    return redirect("/")

def create_trip(request):
    if "first_name" in request.session:
        trip = Trip.objects.create_trip(request.POST, request.session['id'])
        if trip[0] == False:
            for error in trip[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect("add")
        else:
            return redirect('/success')
    return redirect('/')


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
            return redirect('/success')
    return redirect("/")


def logout(request):
    if 'first_name' in request.session:
        request.session.pop('first_name')
    return redirect('/')
