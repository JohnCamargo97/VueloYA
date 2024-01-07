from django.shortcuts import render, redirect
from lib.forms import UpdateUserVYaForm
from users.forms import userFactForm

def createfacturacion(request):

    if request.method == "POST":
        fact_form = userFactForm(request.POST)

        if fact_form.is_valid():
            fact_form.save()
            return redirect('perfil_user')
    else:
        fact_form = userFactForm()

    context = {
        'form' : fact_form,
    }
    
    return context