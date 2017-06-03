# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Users, Secrets, Likes
from django.db.models import Count
from django.contrib import messages

# Create your views here.
def index(request):
    users = Users.objects.all()
    for user in users:
        print user.first_name
    return render(request, 'secret_app/index.html')

def login(request):
    if request.method == 'POST':
        response = Users.objects.login(request.POST)
        if not response[0]:
            for error in response[1]:
                messages.error(request, error[1])
            return redirect('/')
        else:
            request.session['user'] = {
                "id": response[1].id,
                "first_name": response[1].first_name,
                "last_name": response[1].last_name,
            }
            # print response.first_name
            return redirect('/home')

def register(request):
    if request.method == 'POST':
        response = Users.objects.register(request.POST)
        if not response[0]:
            for error in response[1]:
                messages.error(request, error[1])
            return redirect('/')
        else:
            request.session['user'] = {
                "id": response[1].id,
                "first_name": response[1].first_name,
                "last_name": response[1].last_name,
            }
            return redirect('/home')

def submit(request):
    if request.method == 'POST':
        user_id = Users.objects.get(id=request.session['user']['id'])
        response = Secrets.objects.submit(request.POST, user_id)
        if not response[0]:
            for message in response[1]:
                message.error(request, message[1])
            return redirect('/home')
        else:
            return redirect('/home')


def home(request):
    context = {
        "secrets": Secrets.objects.all(),
        "currentUser": Users.objects.get(id=request.session['user']['id']),
        "author": Secrets.objects.randAuthor()
    }
    return render(request, 'secret_app/secrets.html', context)

def popular(request):
    context = {
        "secrets": Secrets.objects.annotate(likes=Count("sec_like")).order_by('-likes'),
        "currentUser": Users.objects.get(id=request.session['user']['id']),
        "author": Secrets.objects.randAuthor()
    }
    return render(request, 'secret_app/popular.html', context)

def like(request, page, id):
    user_id = Users.objects.get(id=request.session['user']['id'])
    sec_id = Secrets.objects.get(id=id)
    Likes.objects.create(user=user_id, secret=sec_id)
    if page == "home":
        return redirect('/home')
    if page == "popular":
        return redirect('/popular')

def delete(request, page, id):
    Secrets.objects.get(id=id).delete()
    if page == "home":
        return redirect('/home')
    if page == "popular":
        return redirect('/popular')
