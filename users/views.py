from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import formUser
from .models import user

def register(request):
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print(form.cleaned_data)

            user = authenticate(usename = username, password = password)
            print(user)
            try:
                login(request, user)
                messages.success(request, ('Registro exitoso'))
                return redirect('home_dev2')
            except:
                messages.success(request, ('valio pija mi compa'))
            
        else:
            messages.error(request, ('Error con el formulario'))        
    else:
        form = UserCreationForm()
        print("empty", form)
    return render(request, 'users/registrarse.html', {'form': form})



def login_user(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home_dev2')
        else:
            messages.error(request, ('Usuario desconocido'))
            return render (request, 'users/iniciarsesion.html')
    else:
        return render (request, 'users/iniciarsesion.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ('Sesion terminada correctamente'))
    return redirect('home_dev2') 


def mensaje_user(request):
    messages.success(request, ('Registrado exitosamente!'))
    return render (request, 'users/mensaje_user.html')

    

