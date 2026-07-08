from django.shortcuts import render
from .models import Course

def course_list(request):
    courses = Course.objects.all()
    return render(request,"course_list.html",{"courses": courses})
def home(request):
    return render(request, "base.html")

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Course
from django.shortcuts import get_object_or_404


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {
            "error": "FALSE"
        })

    return render(request, "login.html")


@login_required
def course_list(request):
    courses = Course.objects.filter(user=request.user)
    return render(request, "course_list.html", {"courses": courses})


def note_create(request):
        if request.mehtod =="POST":
            form =NoteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("note_list")                
        else:
            form=NoreForm()

        return render(request,"note_form.html",{"form":form},)

def note_list(request):
    notes=Note.objects.all()
    return render(request,"notes_list.html",{"notes":notes},)


def note_detail(request,pk):
    note=get_object_or_404(Note,pk=pk)
    return render(request,"note_detail.html",{"note":note})


def note_update(request,pk):
    note=get_object_or_404(Note,pk=pk)
    
    if request.mrthod=="POST":
        form=NoteForm(request,POST,instance=note)
        if form.is_valid():
            form.save()
            return render(request,"note_detail",pk=pk)
        
    else:
        form=NoteForm(instance=note)

    return render(request,"note_form.html",{"form":form},)

def note_delete(request,pk):
    note=get_object_or_404(Note,pk=pk)

    if request.mrthod=="POST":
        note.delete()
        return render("note_list")
    
    return render(request,"note_confirm_delete.html",{"note":note},)

