from django.shortcuts import render, redirect
#from django.http import HttpResponse
from .models import Vuelo
from .forms import BusquedaForm

# Create your views here.

def home(request):
    form_busqueda = BusquedaForm(request.POST or None)
    lista_vuelos = Vuelo.objects.all()
    #print(form_busqueda["origen"])
    return render(request, 'paginas/home.html', {'lista_vuelos': lista_vuelos, 'form_busqueda': form_busqueda})

def home_dev2(request):
    
    if request.method == "POST":

        # if this is a POST request we need to process the form data
        form_busqueda = BusquedaForm(request.POST)
        
        if form_busqueda.is_valid():
                     
            request.session['origen'] = request.POST['origen']
            request.session['destino'] = request.POST['destino']
            print("session updated")

            return redirect('resultados')
        else:
            print("campos no validos")
    else:
        form_busqueda = BusquedaForm()

 
    lista_vuelos = Vuelo.objects.all()
    return render(request, 'paginas/home_dev2.html', {'lista_vuelos': lista_vuelos, 'form_busqueda': form_busqueda})


def resultados(request):

    form_response = request.session
    if form_response['destino']:
        print(form_response['destino'])
    else:
        print(0)
    lista_resultado = Vuelo.objects.filter(origen__icontains = form_response['origen'], destino__icontains = form_response['destino']).values()
    #print(form_response)
    return render (request, 'paginas/resultados.html', {'lista_resultado': lista_resultado, 'form_response': form_response})


def misviajes(request):
    return render (request, 'paginas/misviajes.html')

def iniciarsesion(request):
    return render (request, 'paginas/iniciarsesion.html')

def registrarse(request):
    return render(request, 'paginas/registrarse.html')

def busqueda(request):
    return render(request, 'paginas/busqueda.html')