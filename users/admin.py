from django.contrib import admin
from .models import Feedback

class FeedbackModelAdmin(admin.ModelAdmin):
  list_display = ("name", "email", "comment")
  list_filter = ('name','email')
admin.site.register(Feedback, FeedbackModelAdmin)
