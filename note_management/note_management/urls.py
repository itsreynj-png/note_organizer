from django.contrib import admin
from django.urls import path
from notes import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),

    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),

    path("courses/", views.course_list, name="course_list"),

    path("notes/", views.note_list, name="note_list"),
    path("notes/create/", views.note_create, name="note_create"),
    path("notes/<int:pk>/", views.note_detail, name="note_detail"),
    path("notes/<int:pk>/edit/", views.note_update, name="note_update"),
    path("notes/<int:pk>/delete/", views.note_delete, name="note_delete"),
]