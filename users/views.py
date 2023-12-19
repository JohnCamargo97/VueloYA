from django.shortcuts import render, redirect
from django.contrib import messages
#from django.contrib.auth import authenticate, login, logout
from .forms import formUser
from .models import user

def register(request):
    
    if request.method == "POST":
        form = formUser(request.POST or None)
        if form.is_valid():
              
            usuario_repetido = user.objects.filter(email = request.POST['email']).values()

            if usuario_repetido:
                messages.error(request, ('Este usuario ya existe'))
            else:
                request.session['username'] = request.POST['username']
                print(request.session['username'])
                form.save()
                return redirect('mensaje_user')
        
    else:
        form = formUser()
    return render(request, 'users/registrarse.html', {'form': form})



def login_user(request):

    if request.method == "POST":
        form = formUser(request.POST or None)
        username = request.POST["username"]
        password = request.POST["password"]
        Auth_user = user.objects.filter(username = username, password = password).values()

        if Auth_user:
            request.session['username'] = username
            return redirect('home_dev2')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, ('Usuario desconocido'))
            return render (request, 'users/iniciarsesion.html')
    else:
        form = formUser()
        return render (request, 'users/iniciarsesion.html', {'form': form})

    


def mensaje_user(request):
    messages.success(request, ('Registrado exitosamente!'))
    return render (request, 'users/mensaje_user.html')

    

