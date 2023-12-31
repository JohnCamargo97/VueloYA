from django.shortcuts import render, redirect
#from django.http import HttpResponse
from .models import Vuelo, aerolinea, puestos
from .forms import BusquedaForm


# Create your views here.

def home(request):
    if request.method == "POST":

        # if this is a POST request we need to process the form data
        form_busqueda = BusquedaForm(request.POST)
        
        if form_busqueda.is_valid():
                     
            request.session['origen'] = request.POST['origen']
            request.session['destino'] = request.POST['destino']
            print("session updated")

            return redirect('busqueda')
        else:
            print("campos no validos")
    else:
        form_busqueda = BusquedaForm()

    lista_vuelos = Vuelo.objects.all()
    return render(request, 'paginas/home.html', {'lista_vuelos': lista_vuelos, 'form_busqueda': form_busqueda})

def resultados(request):

    form_response = request.session
    #lista_resultado = Vuelo.objects.filter(origen__icontains = form_response['origen'], destino__icontains = form_response['destino'])
    lista_resultado = Vuelo.objects.filter(origen__icontains = form_response['origen'], destino__icontains = form_response['destino']).all()
    print(lista_resultado)
    return render (request, 'paginas/resultados.html', {'lista_resultado': lista_resultado, 'form_response': form_response})

def misviajes(request):
    return render (request, 'paginas/misviajes.html')

def pagos(request):
    VueloSeleccionado = request.session
    DetallesVuelo = Vuelo.objects.get(pk=VueloSeleccionado['vueloID'])
    return render (request, 'paginas/pagos.html', {'DetallesVuelo': DetallesVuelo})

def busqueda(request):
    form_response = request.session
    lista_resultado = Vuelo.objects.filter(origen__icontains = form_response['origen'], destino__icontains = form_response['destino']).all()
    if request.method == "POST":
        request.session['vueloID'] = request.POST['Comprar']
        return redirect('pagos')
    else:
        return render (request, 'paginas/busqueda.html', {'lista_resultado': lista_resultado, 'form_response': form_response})
