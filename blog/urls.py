from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView ,PostbyUserView
from . import views

urlpatterns = [
    path('', PostListView, name='blog-home'),
    path('post/<int:id>/', PostDetailView, name='post-detail'),
    path('post/new/', PostCreateView, name='post-create'),
    path('post/<int:id>/update/', PostUpdateView, name='post-update'),
    path('post/<int:id>/delete/', PostDeleteView, name='post-delete'),
    path('post/user/<str:username>/',PostbyUserView,name='posts-by-user'),
    path('about/',views.about,name='blog-about'),
]

# py manage.py runserver
# py manage.py migrate
# py manage.py createsuperuser
# py manage.py startapp blog
# django-admin startproject django_project

#py manage.py makemigrations (creates a migration file)
#py manage.py sqlmigrate blog 0001 (to view the sql code for data migration)
#py manage.py migrate (changes takes place in actual database)

#py manage.py shell
# exit() -> to exit from shell
# uvicorn django_project.asgi:application

