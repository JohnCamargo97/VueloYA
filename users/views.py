from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegUserForm, UpdateUserForm
from lib.forms import UpdateUserVYaForm
from users.forms import userFactForm
from django.contrib.auth.models import User

def register(request):
    
    if request.method == "POST":
        form = RegUserForm(request.POST)
        
        if form.is_valid():
            
            user = form.save()
            try:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                print("registro exitoso")
                return redirect('home')
            except:
                messages.success(request, ('Error creando usuario'))
                print("Error con logueo")
            
        else:
            messages.error(request, ('Error con el formulario'))
            print("Formulario invalido", request.POST)

    else:
        form = RegUserForm()
        print("no post request")
    return render(request, 'users/registrarse.html', {'form': form})

def login_user(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, ('Usuario o contraseña incorrecta'))
            return render (request, 'users/iniciarsesion.html')
    else:
        return render (request, 'users/iniciarsesion.html', {})

def logout_user(request):
    logout(request)
    return redirect('home') 

def mensaje_user(request):
    messages.success(request, ('Registrado exitosamente!'))
    return render (request, 'users/mensaje_user.html')

def perfil_user(request):
    return render (request, 'users/perfil_user.html')

def personal_info(request):
 
    if request.method == "POST":
        u_form = UpdateUserForm(request.POST, instance=request.user)
        uvy_form = UpdateUserVYaForm(request.POST, request.FILES, instance=request.user.uservueloya)

        if u_form.is_valid() and uvy_form.is_valid():
            u_form.save()
            uvy_form.save()
            return redirect('perfil_user')
    else:
        u_form = UpdateUserForm(instance=request.user)
        uvy_form = UpdateUserVYaForm(instance=request.user.uservueloya)

    context = {
        'u_form' : u_form,
        'uvy_form' : uvy_form
    }
    return render (request, 'users/personal-info.html', context)

def facturacion(request):
    if request.method == "POST":
        fact_form = userFactForm(request.POST, instance=request.user)

        if fact_form.is_valid():
            fact_form.save()
            return redirect('perfil_user')
        else:
            print ('not valid')
    else:
        fact_form = userFactForm(instance=request.user)

    context = {
        'form' : fact_form,
    }
    
    return render (request, 'users/facturacion.html', context)