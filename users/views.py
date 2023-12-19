from django.shortcuts import render, redirect
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from .forms import formRegistro

def register(request):
    
    if request.method == "POST":
        form = formRegistro(request.POST or None)
        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('mensaje_user')
        
    else:
        form = formRegistro()
    return render(request, 'users/register.html', {'form': form})


def mensaje_user(request):
    messages.success(request, ('Registrado exitosamente!'))
    return render (request, 'users/mensaje_user.html')

    

