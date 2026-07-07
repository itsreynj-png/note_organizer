from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth import UserCreationForm,AuthenticationForm

def register(request):
    if request.method=="POST":
        form =UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)    
    else:
        form =UserCreationForm()
    return render(request,"register.html",{"form":form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")