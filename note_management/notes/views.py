from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Course, Note
from .forms import NoteForm
from django.db.models import Q



def home(request):
    return render(request, "base.html")


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
            password=password,
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

    return render(
        request,
        "course_list.html",
        {"courses": courses},
    )


@login_required
def note_create(request):
    if request.method == "POST":

        form = NoteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("note_list")

    else:

        form = NoteForm()

    return render(
        request,
        "note_form.html",
        {"form": form},
    )


@login_required
def note_list(request):
    query =request.GET.get("q")
    notes = Note.objects.filter(course__user=request.user)

    if query:
        notes = notes.filter(Q(title__icontains=query)|Q(content__icontains=query))


    return render(
        request,
        "note_list.html",
        {"notes": notes,
        "query":query},
    )


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)

    return render(
        request,
        "note_detail.html",
        {"note": note},
    )


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":

        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            form.save()
            return redirect("note_detail", pk=pk)

    else:

        form = NoteForm(instance=note)

    return render(
        request,
        "note_form.html",
        {"form": form},
    )


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        note.delete()
        return redirect("note_list")

    return render(
        request,
        "note_confirm_delete.html",
        {"note": note},
    )
