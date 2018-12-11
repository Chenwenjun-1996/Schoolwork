from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def display(request):
    return render(request, 'displayMap.html')


def drawMap(request):
    if request.method == 'POST':
        pass
    return render(request, 'map.html')