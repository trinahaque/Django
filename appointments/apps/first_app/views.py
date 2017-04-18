from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date
from django.utils import formats
from .models import User, Appointment

def index(request):
    if 'first_name' in request.session:
        return redirect('/success')
    return render(request, "first_app/index.html")

def success(request):
    if 'first_name' in request.session:
        today = datetime.today()
        request.session['today'] = formats.date_format(today, 'DATE_FORMAT')
        appointments = Appointment.objects.filter(user_id=request.session['id'], date=unicode(datetime.today().date())).order_by("-time").reverse()
        # appointments is a list of appointment objects
        other_appointments = Appointment.objects.filter(user_id=request.session['id']).exclude(date=unicode(datetime.today().date())).order_by("-date","-time").reverse()
        context = {
            "appointments": appointments,
            "other_appointments": other_appointments
        }
        return render(request, "first_app/success.html", context)
    return redirect('/')

def add(request, id):
    if 'first_name' in request.session:
        user_id = id
        appointment = Appointment.objects.appointment_valid(request.POST, user_id)
        if appointment[0] == False:
            for error in appointment[1]:
                messages.add_message(request, messages.INFO, error)
        return redirect('/success')
    return redirect('/')

def edit(request, aid, id):
    if "first_name" in request.session:
        appointment = Appointment.objects.get(id=aid, user_id = id)
        # This is a single appointment object
        context = {
            "appointment": appointment
        }
        return render(request, "first_app/update.html", context)
    return redirect('/')

def update(request, aid, id):
    # why is it redirecting to success
    if "first_name" in request.session:
        updated_appointment = Appointment.objects.update_app(request.POST, id, aid)
        if updated_appointment[0] == False:
            for error in updated_appointment[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('edit', aid=aid, id=id)
        else:
            return redirect("/success")
    return redirect('/')

def delete(request, aid, id):
    if "first_name" in request.session:
        Appointment.objects.get(id=aid, user_id=id).delete()
        return redirect("/success")
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
            request.session['id'] = result[1].id
            print request.session['id']
            request.session['first_name']= result[1].first_name
            return redirect('/success')
    return redirect("/")


def logout(request):
    if 'first_name' in request.session:
        request.session.pop('first_name')
    return redirect('/')
