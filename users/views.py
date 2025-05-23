from django.shortcuts import render
#from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import FeedbackForm  
from .models import Feedback

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = Feedback(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                comment=form.cleaned_comment(form)
            )
            feedback.save()
            return HttpResponse("Спасибо за ваш отзыв!")
        else:
            return render(request, 'feedback.html', {'form': form})
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form})
