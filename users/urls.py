from django.urls import path
from . import views

urlpatterns = [
    path('feedback/', views.feedback_post, name='users'),
    path('feedback/<pk>', views.feedback_edit, name='users'),
]
