from django.shortcuts import render

from profile_app.models import book

# Create your views here.

def index(request):
    return render(request,'index.html')