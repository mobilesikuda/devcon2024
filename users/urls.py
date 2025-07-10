from django.urls import path
from . import views

urlpatterns = [
    path('feedback/post', views.feedback_post, name='users'),
    path('feedback/edit/<pk>', views.feedback_edit, name='users'),
]
