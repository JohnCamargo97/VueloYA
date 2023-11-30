from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'paginas/home.html')

def misviajes(request):
    return render (request, 'paginas/misviajes.html')

def iniciarsesion(request):
    return render (request, 'paginas/iniciarsesion.html')

def registrarse(request):
    return render(request, 'paginas/registrarse.html')