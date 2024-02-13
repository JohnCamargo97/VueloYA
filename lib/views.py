from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q
from .models import Vuelo, historicoReserva, oferta, aerolinea
from django_filters.views import FilterView
from .filter import vueloFilter
from users.models import pasajero
from .forms import BusquedaForm, filtroForm, voucherForm, metodoPago, datosTarjeta, terminosyCondiciones
from users.forms import userPasajeroForm
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


class resultado(FilterView):
    model= Vuelo
    template_name= "paginas/busqueda.html"
    context_object_name = "lista_resultado"
    filterset_class = vueloFilter

    def get_queryset(self, **kwargs):
        print("request.GET: ",self.request.GET)
        return Vuelo.objects.filter(origen__icontains = self.kwargs["origen"], destino__icontains = self.kwargs["destino"]).all()

    def get_context_data(self, **kwargs):
        context = super(resultado, self).get_context_data(**kwargs)
        context['origen'] = self.kwargs["origen"]
        context['destino'] = self.kwargs["destino"]
        context['aerolineas'] = Vuelo.objects.filter(origen__icontains = self.kwargs["origen"], destino__icontains = self.kwargs["destino"]).annotate(conteo=Count('id_aerolinea')).values_list("id_aerolinea__nombre_aerolinea", "id_aerolinea", "conteo")

        return context

    def get(self, request, *args, **kwargs):
        print("request.GET: ",request.GET)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        print("request POST:", request)
        ctxt = {}
        ctxt['method'] = "post"
        
        if 'busqueda' in request.POST:
            form_busqueda = BusquedaForm(request.POST)

            if form_busqueda.is_valid():
                return redirect('busqueda', request.POST['origen'], request.POST['destino'], request.POST['pasajeros'])

            return render(self.request, self.template_name, self.get_context_data())




class busqueda(View):
    def get(self, request, *args, **kwargs):
        lista_resultado = Vuelo.objects.filter(origen__icontains = self.kwargs["origen"], destino__icontains = self.kwargs["destino"]).all()

        if request.method == "POST":
            form_busqueda = BusquedaForm(request.POST)
            form_filtro = filtroForm(request.POST)
            print(request.POST)
            if form_filtro.is_valid():
                print(form_filtro.cleaned_data)

            if form_busqueda.is_valid():
                request.session['origen'] = request.POST['origen']
                request.session['destino'] = request.POST['destino']
                request.session['pasajeros'] = request.POST['pasajeros']    
                return redirect('busqueda', request.POST['origen'], request.POST['destino'], request.POST['pasajeros'])
            
        else:
            form_busqueda = BusquedaForm()
            form_filtro = filtroForm()

            AEROLINEAS = Vuelo.objects.filter(origen__icontains = self.kwargs["origen"], destino__icontains = self.kwargs["destino"]).annotate(conteo=Count('id_aerolinea')).values_list("id_aerolinea__nombre_aerolinea", "conteo")
            print(AEROLINEAS)
            context = {
            'origen': self.kwargs["origen"],
            'destino': self.kwargs["destino"],
            'aerolineas': AEROLINEAS,
            'form_filtro': form_filtro,
            'lista_resultado': lista_resultado
        }
            return render(request, 'paginas/busqueda.html', context)


def resumen(request):
    return render (request, 'paginas/resumen.html')
