from django.shortcuts import render
from .models import *

# Create your views here.
def blog(request):
    views = {}
    return render(request, 'index.html', views)
