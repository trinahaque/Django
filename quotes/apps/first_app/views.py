from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote, Favorite


def index(request):
    if 'first_name' in request.session:
        return redirect('/success')
    return render(request, "first_app/index.html")

def success(request):
    if 'first_name' in request.session:
        quotes = Quote.objects.exclude(favorite__user_id=request.session['id'])
        favorites = Favorite.objects.filter(user_id=request.session['id'])
        context = {
            "quotes": quotes,
            "favorites": favorites
        }
        return render(request, "first_app/success.html", context)
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

def quotes(request, id):
    quote_by = request.POST['quote_by']
    message = request.POST['quote']
    if len(quote_by) < 3 or len(message) < 10:
        if len(quote_by) < 3:
            messages.warning(request, 'Quote by needs to be at least three characters')
        if len(message) <10:
            messages.warning(request, 'Message needs to be at least ten characters')
    else:
        user = User.objects.get(id=id)
        add_quote = Quote.objects.create(quote_by=request.POST['quote_by'], quote=request.POST['quote'], user=user)
    return redirect('/success')

def favorite(request, id, qid):
    user = User.objects.get(id=id)
    quote = Quote.objects.get(id=qid)
    add_favorite = Favorite.objects.create(user=user, quote=quote)
    return redirect('/success')

def remove(request, id, qid):
    user = User.objects.get(id=id)
    quote = Quote.objects.get(id=qid)
    remove = Favorite.objects.filter(user=user, quote=quote).delete()
    return redirect('/success')

def users(request, id):
    user = User.objects.get(id=id)
    quotes = Quote.objects.filter(user_id=id)
    request.session['count'] = len(quotes)
    context = {
        'user': user,
        'quotes': quotes
    }
    return render(request, 'first_app/users.html', context)

def logout(request):
    if 'first_name' in request.session:
        request.session.pop('first_name')
    return redirect('/')
