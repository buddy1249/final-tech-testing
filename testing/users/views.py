from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginUserForms
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# Create your views here.

def login_user(request):
    if request.method == "POST":
        form = LoginUserForms(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
         form = LoginUserForms()        
            
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))