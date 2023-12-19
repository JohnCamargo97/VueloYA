from django.shortcuts import render, redirect
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from .forms import formRegistro
from .models import user

def register(request):
    
    if request.method == "POST":
        form = formRegistro(request.POST or None)
        if form.is_valid():
              
            usuario_repetido = user.objects.filter(email = request.POST['email']).values()
            if usuario_repetido:
                messages.error(request, ('Este usuario ya existe'))
            else:
                request.session['email'] = request.POST['email']
                request.session['fullname'] = request.POST['fullname']
                print(request.POST)
                form.save()
                return redirect('mensaje_user')
        
    else:
        form = formRegistro()
    return render(request, 'users/register.html', {'form': form})


def mensaje_user(request):
    messages.success(request, ('Registrado exitosamente!'))
    return render (request, 'users/mensaje_user.html')

    

