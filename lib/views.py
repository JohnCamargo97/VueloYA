from django.shortcuts import render, redirect
from django.db.models.query import EmptyQuerySet
from django.contrib.auth.models import User
from .models import Vuelo, aerolinea, puestos
from users.models import pasajero
from .forms import BusquedaForm
from users.forms import userPasajeroForm
from django.forms import modelformset_factory

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
    return render (request, 'paginas/resumen.html')
    
def pagos(request):
    VueloSeleccionado = request.session
    nPasajeros = int(VueloSeleccionado['pasajeros'])
    PasajeroFormSet = modelformset_factory(pasajero, form= userPasajeroForm, extra=nPasajeros)
    DetallesVuelo = Vuelo.objects.get(pk=VueloSeleccionado['vueloID'])
    if request.method == "POST":
        print("Posted", request.POST)
        pasaje = PasajeroFormSet(request.POST, EmptyQuerySet)
        for pas in pasaje:
            if pas.is_valid():
                print(pas.cleaned_data)
                pas1 = pas.save(commit= False)
                pas1.user = request.user
                pas1.save()
    
            else:
                print("no valido")
        return redirect('resumen')
    else:
        pasaje = PasajeroFormSet(queryset= EmptyQuerySet)
        print("not posted")
    
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
