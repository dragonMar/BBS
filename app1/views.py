from django.shortcuts import render
from django.shortcuts import render_to_response
from app1 import models
# Create your views here.


def index(request):
    all_data = models.News.objects.all()
    return render_to_response('index.html',{'data': all_data})