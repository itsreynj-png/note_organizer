from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Course, Note
from .forms import NoteForm ,CourseForm
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
            "error": "Invalid Username or Password"
        })

    return render(request, "login.html")


@login_required
def course_create(request):
    if request.method == "POST":

        form =CourseForm(request.POST)

        if form.is_valid():
            course=form.save(commit=False)
            course.user=request.user
            course.save()
            return redirect("course_list")

    else:

        form = CourseForm()

    return render(
        request,
        "course_form.html",
        {"form": form},
    )


@login_required
def course_detail(request,pk):
    course=get_object_or_404(Course,pk=pk)
    notes = Note.objects.filter(course=course)

    return render(request,
                  "course_detail.html",
                  {"course":course,
                   "notes":notes},
    )


@login_required
def course_list(request):
    courses = Course.objects.filter(user=request.user)

    return render(
        request,
        "course_list.html",
        {"courses": courses},
    )


@login_required
def course_update(request,pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":

        form = CourseForm(request.POST, instance=course)

        if form.is_valid():
            update_course=form.save(commit=False)
            update_course.user=course.user
            update_course.save()
            return redirect("course_detail", pk=pk)

    else:

        form = CourseForm(instance=course)

    return render(
        request,
        "course_form.html",
        {"form": form},
    )


@login_required
def course_delete(request,pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.delete()
        return redirect("course_list")

    return render(
        request,
        "course_confirm_delete.html",
        {"course": course},
    )



@login_required
def note_create(request,course_id):
    course=get_object_or_404(Course,id=course_id)
    if request.method == "POST":

        form = NoteForm(request.POST)

        if form.is_valid():
            note=form.save(commit=False)
            note.course=course
            note.save()
            return redirect("note_list")

    else:

        form = NoteForm()

    return render(
        request,
        "note_create.html",
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
            update_note=form.save(commit=False)
            update_note.course=note.course
            update_note.save()
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