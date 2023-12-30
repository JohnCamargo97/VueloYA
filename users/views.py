from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegUserForm
from django.contrib.auth.models import User

def register(request):
    
    if request.method == "POST":
        form = RegUserForm(request.POST)
        
        if form.is_valid():
            
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print("form valid")

            #user = authenticate(usename = username, password = password)
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
    if request.user.is_authenticated:
        actual_user = User.objects.get(id=request.user.id)
        form = RegUserForm(request.POST or None, instance= actual_user)
        if form.is_valid():
            form.save()
            login(request, actual_user)
            return redirect('perfil_user')

        return render (request, 'users/personal-info.html', {'form': form})

    else:
        return redirect('iniciarsesion')
    
#def update_user(request):
