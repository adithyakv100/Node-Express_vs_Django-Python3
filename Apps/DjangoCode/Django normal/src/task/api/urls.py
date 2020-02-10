from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from task.api import views


urlpatterns = [
    path('', views.TaskListView.as_view()),
    path('create', views.TaskCreate.as_view()),
    path('<int:id>/status', views.TaskUpdate.as_view()),


]
