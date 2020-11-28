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

import numpy as np
import torch
from torchvision import transforms
from PIL import Image

longitud, altura = 224, 224
PATH = 'modelo_completo.pth'

mean = np.array([0.5, 0.5, 0.5])
std = np.array([0.25, 0.25, 0.25])


Test = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])



model = torch.load(PATH)
model.eval()

def predict(file):

  img = Test(Image.open(file))
  batch_img_tensor = torch.unsqueeze(img, 0)  # 0 es el AXIS. 
  out = model(batch_img_tensor)
  
  array = out.detach().numpy()
  print(array[0][1])    #[0][0] es la probabilidad de que sea BENIGNO
  return array[0][1]

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
            diagnosis = predict(imagen)
            

            messages.success(request, diagnosis)

            

    else:
        form = operacionform() #Si no es un metodo post, devuelve el coso vacio. 

    return render(request, 'myform/cxform.html', {'form':form})
