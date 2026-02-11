"""
URL configuration for DjangoProject project.

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
from DjangoApp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("getAllTasks/", views.getAllTasks, name="getAllTasks"),
    path("addTask/", views.addTask, name="addTask"),
    path('deleteTask/<int:id>/', views.deleteTask, name='deleteTask'),
    path('editTask/<int:id>/', views.editTask, name='editTask'),
    path('getTeamsTasks/<str:team>/', views.getTeamsTasks, name='getTeamsTasks'),
    path('personalArea/', views.personalArea, name='personalArea'),
    path('taskAssignment/<int:task_id>/', views.taskAssignment, name='taskAssignment'),
    path('changeStatus/<int:task_id>/<str:status>/', views.changeStatus, name='changeStatus'),
    path('filterByStatus/<str:status>/', views.filterByStatus, name='filterByStatus'),
    path('filterByWorker/<str:username>/', views.filterByWorker, name='filterByWorker'),
]
