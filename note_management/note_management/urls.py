"""
URL configuration for note_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from notes.views import home
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home),
]

from notes.views import course_list

urlpatterns=[
    path("admin/", admin.site.urls),
    path("",course_list,name="course_list"),
]

from notes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.course_list, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
]



urlpatterns = [
    path("", views.note_list, name="note_list"),
    path("create/", views.note_create, name="note_create"),
    path("<int:pk>/", views.note_detail, name="note_detail"),
    path("<int:pk>/edit/", views.note_update, name="note_update"),
    path("<int:pk>/delete/", views.note_delete, name="note_delete"),
]