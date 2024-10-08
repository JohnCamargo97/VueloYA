from typing import Any
from datetime import datetime
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from django.views.generic import ListView
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Q
from django.forms import formset_factory
from .models import Vuelo, historicoReserva, oferta, lugarTuristico, aerolinea, puestos
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
    lista_vuelos_origen = Vuelo.objects.all().values("origen").annotate(conteo=Count('origen'))
    lista_vuelos_destino = Vuelo.objects.all().values("destino").annotate(conteo=Count('destino'))

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
        'form_busqueda': form_busqueda,
        'vuelos_origen': lista_vuelos_origen,
        'vuelos_destino': lista_vuelos_destino
    }
    return render(request, 'paginas/home.html', context)


def misviajes(request):
    lista = historicoReserva.objects.filter(user = request.user).all()
    return render(request, 'paginas/misviajes.html', {'lista': lista})


def viajes_borrar(request, pk):
    if request.user.is_authenticated:
        reserva = get_object_or_404(historicoReserva, id= pk)
        if request.user.id == reserva.user_id:    
            reserva.delete()
            return redirect('misviajes')
        else:
            return redirect('misviajes')
    else:
        return redirect('home')

@login_required
def pagos(request, pk):
    VueloSeleccionado = request.session
    nPasajeros = int(VueloSeleccionado['pasajeros'])
    detallesVuelo = Vuelo.objects.get(pk=pk)
    PUESTOS = puestos.objects.filter(Vuelo_id = pk).annotate(conteo=Count('pasajero')).values_list("id", 'Ventana_bool', 'conteo').filter(conteo = 0)
    inicio = datetime.combine(detallesVuelo.fechasalida, detallesVuelo.horasalida1)
    final = datetime.combine(detallesVuelo.fechavuelta, detallesVuelo.horavuelta2)
    duracion = final - inicio
    total = detallesVuelo.precio * nPasajeros
    extra = total*0.19
    userpasajeroset = formset_factory(userPasajeroForm, extra=nPasajeros)
    print("detalles-precio: ", detallesVuelo.precio, nPasajeros, PUESTOS)
    if request.method == "POST":
        print("POSTED")
        formset_response = userpasajeroset(request.POST)
        uservoucherForm =  voucherForm(request.POST)
        usermetodopagoForm = metodoPago(request.POST)
        userdatostarjetaForm = datosTarjeta(request.POST)
        usertyc = terminosyCondiciones(request.POST)
        if  formset_response.is_valid():
            print('cleaned data: ', formset_response.cleaned_data)
             
            for form in formset_response:
                form_save = form.save(commit= False)
                form_save.user = request.user
                form_save.save()

            if uservoucherForm.is_valid() and usermetodopagoForm.is_valid() and userdatostarjetaForm.is_valid() and usertyc.is_valid():
                print(f'voucher: {uservoucherForm.cleaned_data}, metodo: {usermetodopagoForm.cleaned_data}, tarjeta: {userdatostarjetaForm.cleaned_data}, tyc: {usertyc.cleaned_data}')
                Reserva = historicoReserva(user= request.user, vuelo= detallesVuelo, puestos= pasajero.puesto, pasajeros= nPasajeros, estado="Reservado", total=nPasajeros*detallesVuelo.precio, duracion= duracion)
                Reserva.save()
                return redirect('resumen')
            else:
                print("error con formularios")
        else:
            print("errors: ", formset_response.non_form_errors(), formset_response.errors )
        
    else:
        formset_response = userpasajeroset()
        uservoucherForm =  voucherForm()
        usermetodopagoForm = metodoPago()
        userdatostarjetaForm = datosTarjeta()
        usertyc = terminosyCondiciones()


    context = {
        'total': total,
        'extra': extra,
        'DetallesVuelo': detallesVuelo,
        'puestos': PUESTOS,
        'userpasajeroFormset': formset_response,
        'uservoucherForm': uservoucherForm,
        'usermetodopagoForm': usermetodopagoForm,
        'userdatostarjetaForm': userdatostarjetaForm,
        'tyc': usertyc
    }
    print('context: ', context)
    return render (request, 'paginas/pagos.html', context)

class PaginatedFilterViews(View):
    def get_context_data(self, **kwargs):
        context = super(PaginatedFilterViews, self).get_context_data(**kwargs)
        if self.request.GET:
            querystring = self.request.GET.copy()
            if self.request.GET.get('page'):
                del querystring['page']
            context['querystring'] = querystring.urlencode()
            context['dec_querystring'] = querystring
        return context

class resultado(PaginatedFilterViews, FilterView):
    model= Vuelo
    template_name= "paginas/busqueda.html"
    #context_object_name = "lista_resultado"
    filterset_class = vueloFilter
    paginate_by = 5

    def get_queryset(self, **kwargs):
        queryset = Vuelo.objects.filter(origen__icontains = self.kwargs["origen"], destino__icontains = self.kwargs["destino"]).all()
        #filter = vueloFilter( self.request.GET, queryset= queryset1 ).qs
        return queryset

    def get_context_data(self, **kwargs):
        print("running context")

        #Turismo del destino
        turismos = lugarTuristico.objects.filter(vuelo__destino = self.kwargs["destino"]).all()

        context = super(resultado, self).get_context_data(**kwargs)
        context['origen'] = self.kwargs["origen"]
        context['destino'] = self.kwargs["destino"]
        context['turismos'] = turismos
        context['aerolineas'] =  Vuelo.objects.filter(origen__icontains = self.kwargs["origen"], destino__icontains = self.kwargs["destino"]).values("id_aerolinea__nombre_aerolinea", "id_aerolinea").annotate(conteo=Count('id_aerolinea')).values_list("id_aerolinea__nombre_aerolinea", "id_aerolinea", "conteo")
        context['vuelos_origen'] = lista_vuelos_origen = Vuelo.objects.all().values("origen").annotate(conteo=Count('origen'))
        context['vuelos_destino'] = lista_vuelos_destino = Vuelo.objects.all().values("destino").annotate(conteo=Count('destino'))
        print("getContext: ", context)
        return context

    #def get(self, request, *args, **kwargs):
    #    print("request.GET: ", self.request.GET)
    #    return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        print("request POST:", request)
        ctxt = {}
        ctxt['method'] = "post"
        
        if 'busqueda' in request.POST:
            form_busqueda = BusquedaForm(request.POST)

            if form_busqueda.is_valid():
                request.session['pasajeros'] = request.POST['pasajeros'] 
                return redirect('busqueda', request.POST['origen'], request.POST['destino'], request.POST['pasajeros'])

            return render(self.request, self.template_name, self.get_context_data())

def footer(request):
    return render (request, "paginas/footer.html")

def resumen(request):
    return render (request, 'paginas/resumen.html')