from typing import Any
from datetime import datetime
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q
from django.forms import formset_factory
from .models import Vuelo, historicoReserva, oferta, aerolinea, puestos
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


def pagos(request, pk):
    VueloSeleccionado = request.session
    nPasajeros = int(VueloSeleccionado['pasajeros'])
    detallesVuelo = Vuelo.objects.get(pk=pk)
    PUESTOS = puestos.objects.filter(Vuelo_id = pk).values_list("id", 'Ventana_bool')
    inicio = datetime.combine(detallesVuelo.fechasalida, detallesVuelo.horasalida1)
    final = datetime.combine(detallesVuelo.fechavuelta, detallesVuelo.horavuelta2)
    duracion = final - inicio
    total = detallesVuelo.precio * nPasajeros
    extra = total*0.19
    userpasajeroset = formset_factory(userPasajeroForm, extra=nPasajeros)
    print("detalles-precio: ", detallesVuelo.precio, nPasajeros, PUESTOS)
    if request.method == "POST":
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
            print("errors: ", formset_response.non_form_errors(), formset_response.errors)
        
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

class resultado(FilterView):
    model= Vuelo
    template_name= "paginas/busqueda.html"
    context_object_name = "lista_resultado"
    filterset_class = vueloFilter
    paginate_by = 1

    def get_queryset(self, **kwargs):
        print("request.GET: ",self.request.GET)
        return Vuelo.objects.filter(origen__icontains = self.kwargs["origen"], destino__icontains = self.kwargs["destino"]).all()

    def get_context_data(self, **kwargs):
        context = super(resultado, self).get_context_data(**kwargs)
        context['origen'] = self.kwargs["origen"]
        context['destino'] = self.kwargs["destino"]
        context['aerolineas'] =  Vuelo.objects.filter(origen__icontains = self.kwargs["origen"], destino__icontains = self.kwargs["destino"]).annotate(conteo=Count('id_aerolinea')).values_list("id_aerolinea__nombre_aerolinea", "id_aerolinea", "conteo")

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
                request.session['pasajeros'] = request.POST['pasajeros'] 
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


def footer(request):
    return render (request, "paginas/footer.html")


def resumen(request):
    return render (request, 'paginas/resumen.html')