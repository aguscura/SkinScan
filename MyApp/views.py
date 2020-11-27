from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from . models import imagen
from . serializers import operacionSerializers
from . forms import operacionform
import pickle
import json
import numpy as np
from django.contrib import messages

# Create your views here.


class operacionViews(viewsets.ModelViewSet):
    queryset = imagen.objects.all() #Cada vez que pida una requests van a estar TODOS los objetos puestos en Operacion. 
    serializer_class = operacionSerializers #Y usará el OperacionSerializer.


# def approvereject(dic): #Funcion que le doy la request y me dice si está OK.

#     try:

#     except ValueError as error:

#         return Response(error.args[0], status.HTTP_400_BAD_REQUEST) 

        

def cxcontact(request): #En vez de usar el decorador de arriba, que solo servía para POST, este me va a dejar cualquier request.
    
    if request.method == "POST": #Si es un metodo post, arma un form con todos los datos.
        form = operacionform(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            data = form.cleaned_data
            imagen = data["imagen"]
            
            
            messages.success(request, "Formulario enviado correctamente")
            # respuesta = approvereject() Acá invocar a la funcion de ML.
            

    else:
        form = operacionform() #Si no es un metodo post, devuelve el coso vacio. 

    return render(request, 'myform/cxform.html', {'form':form})
