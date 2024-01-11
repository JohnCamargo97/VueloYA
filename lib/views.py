from django.shortcuts import render, redirect
#from django.http import HttpResponse
from .models import Vuelo, aerolinea, puestos
from .forms import BusquedaForm
from users.forms import userPasajeroForm
from django.forms import formset_factory

def home(request):
    if request.method == "POST":

        # if this is a POST request we need to process the form data
        form_busqueda = BusquedaForm(request.POST)
        
        if form_busqueda.is_valid():
                     
            request.session['origen'] = request.POST['origen']
            request.session['destino'] = request.POST['destino']
            request.session['pasajeros'] = request.POST['pasajeros']
            print(request.POST)

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
    nPasajeros = int(VueloSeleccionado['pasajeros'])
    PasajeroFormSet = formset_factory(userPasajeroForm, extra= nPasajeros)
    DetallesVuelo = Vuelo.objects.get(pk=VueloSeleccionado['vueloID'])
    if request.method == "POST":
        pasaje = PasajeroFormSet(request.POST)
        if pasaje.is_valid():
            pasaje.save()
            return redirect('resumen')
        else:
            print(pasaje.errors)
    else:
        pasaje = PasajeroFormSet()
    
    return render (request, 'paginas/pagos.html', {'DetallesVuelo': DetallesVuelo, 'pasaje': pasaje})

def busqueda(request):
    form_response = request.session
    lista_resultado = Vuelo.objects.filter(origen__icontains = form_response['origen'], destino__icontains = form_response['destino']).all()
    if request.method == "POST":
        request.session['vueloID'] = request.POST['Comprar']
        #request.session['pasajeros'] = form_response['pasajeros']
        return redirect('pagos')
    else:
        return render (request, 'paginas/busqueda.html', {'lista_resultado': lista_resultado, 'form_response': form_response})

def resumen(request):
    return render (request, 'paginas/resumen.html')
