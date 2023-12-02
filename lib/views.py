from django.shortcuts import render
#from django.http import HttpResponse
from .models import Vuelo
# Create your views here.

def home(request):
    lista_vuelos = Vuelo.objects.all()
    #print(lista_vuelos.id)
    return render(request, 'paginas/home.html', {'lista_vuelos': lista_vuelos})

def misviajes(request):
    return render (request, 'paginas/misviajes.html')

def iniciarsesion(request):
    return render (request, 'paginas/iniciarsesion.html')

def registrarse(request):
    return render(request, 'paginas/registrarse.html')