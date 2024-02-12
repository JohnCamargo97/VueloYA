from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q
from .models import Vuelo, historicoReserva, oferta
from users.models import pasajero
from .forms import BusquedaForm, filtroBusquedaForm, voucherForm, metodoPago, datosTarjeta, terminosyCondiciones
from users.forms import userPasajeroForm
from django.forms import modelformset_factory
from random import sample

def home(request):

    #3 ofertas aleatorio con sample y list comprehension
    ofertaIds = sample([offer.id for offer in oferta.objects.all()], 3)
    ofertas = oferta.objects.filter(id__in=ofertaIds).all()
    lista_vuelos = Vuelo.objects.all()

    if request.method == "POST":
        # if this is a POST request we need to process the form data
        form_busqueda = BusquedaForm(request.POST)
        
        if form_busqueda.is_valid():
                     
            request.session['origen'] = request.POST['origen']
            request.session['destino'] = request.POST['destino']
            request.session['pasajeros'] = request.POST['pasajeros']    
            return redirect('busqueda', request.POST['origen'], request.POST['destino'], request.POST['pasajeros'])
        else:
            print("campos no validos")
    else:
        form_busqueda = BusquedaForm()

    context = {
        'ofertas': ofertas,
        'form_busqueda': form_busqueda
    }
    return render(request, 'paginas/home.html', context)

def misviajes(request):
    return render (request, 'paginas/misviajes.html')
    
def pagos(request, pk):
    VueloSeleccionado = request.session
    nPasajeros = int(VueloSeleccionado['pasajeros'])
    detallesVuelo = Vuelo.objects.get(pk=pk)
    if request.method == "POST":
        userpasajeroForm = userPasajeroForm(request.POST)
        uservoucherForm =  voucherForm(request.POST)
        usermetodopagoForm = metodoPago(request.POST)
        userdatostarjetaForm = datosTarjeta(request.POST)
        usertyc = terminosyCondiciones(request.POST)
        if  userpasajeroForm.is_valid():
            print(userpasajeroForm.cleaned_data)
            pasajero = userpasajeroForm.save(commit= False)
            pasajero.user = request.user
            pasajero.save()

            if uservoucherForm.is_valid() and usermetodopagoForm.is_valid() and userdatostarjetaForm.is_valid() and usertyc.is_valid():
                print(f'voucher: {uservoucherForm.cleaned_data}, metodo: {usermetodopagoForm.cleaned_data}, tarjeta: {userdatostarjetaForm.cleaned_data}, tyc: {usertyc.cleaned_data}')
                Reserva = historicoReserva(user= request.user, vuelo= detallesVuelo, puestos= pasajero.puesto, pasajeros= nPasajeros, estado="Reservado")
                Reserva.save()
                return redirect('resumen')
            else:
                print("error con formularios")
        else:
            print(userpasajeroForm.errors)
        
    else:
        userpasajeroForm = userPasajeroForm()
        uservoucherForm =  voucherForm()
        usermetodopagoForm = metodoPago()
        userdatostarjetaForm = datosTarjeta()
        usertyc = terminosyCondiciones()

    context = {
        'detallesVuelo': detallesVuelo,
        'userpasajeroForm': userpasajeroForm,
        'uservoucherForm': uservoucherForm,
        'usermetodopagoForm': usermetodopagoForm,
        'userdatostarjetaForm': userdatostarjetaForm,
        'tyc': usertyc
    }
    
    return render (request, 'paginas/pagos.html', context)

def busqueda(request, origen, destino, pas):


    lista_resultado = Vuelo.objects.filter(origen__icontains = origen, destino__icontains = destino).all()

    if request.method == "POST":
        form_busqueda = BusquedaForm(request.POST)
        form_filtro = filtroBusquedaForm(request.POST)
        print(request.POST)

        if form_busqueda.is_valid() and form_filtro.is_valid():
            request.session['origen'] = request.POST['origen']
            request.session['destino'] = request.POST['destino']
            request.session['pasajeros'] = request.POST['pasajeros']
            request.session['rango_precio'] = request.POST['rango_precio']
            request.session['aerolinea'] = request.POST['aerolinea']
 
            return redirect('busqueda', request.POST['origen'], request.POST['destino'], request.POST['pasajeros'])
        else:
            return render(request, 'paginas/busqueda.html', context)    
    else:
        form_busqueda = BusquedaForm()
        form_filtro = filtroBusquedaForm()

        AEROLINEAS = Vuelo.objects.filter(origen__icontains = origen, destino__icontains = destino).annotate(conteo=Count('id_aerolinea')).values_list("id_aerolinea__nombre_aerolinea", "id_aerolinea", "conteo")
        print(AEROLINEAS)
        context = {
        'origen': origen,
        'destino': destino,
        'aerolineas': AEROLINEAS,
        'form_filtro': form_filtro,
        'lista_resultado': lista_resultado
    }
        return render(request, 'paginas/busqueda.html', context)

def resumen(request):
    return render (request, 'paginas/resumen.html')
