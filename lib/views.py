from django.shortcuts import render
#from django.http import HttpResponse
from .models import Vuelo
from .forms import BusquedaForm

# Create your views here.

def home(request):
    form_busqueda = BusquedaForm(request.POST or None)
    lista_vuelos = Vuelo.objects.all()
    #print(form_busqueda["origen"])
    return render(request, 'paginas/home.html', {'lista_vuelos': lista_vuelos, 'form_busqueda': form_busqueda})

def misviajes(request):
    return render (request, 'paginas/misviajes.html')

def iniciarsesion(request):
    return render (request, 'paginas/iniciarsesion.html')

def registrarse(request):
    return render(request, 'paginas/registrarse.html')