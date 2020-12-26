from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from . models import modelo_imagen
from . serializers import imagenserializer
from . forms import imagenform
import pickle
import json
import numpy as np
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

import numpy as np
import torch
from torchvision import transforms
from PIL import Image

longitud, altura = 224, 224

PATH_1 = 'modelo_completo_1er.pth'
PATH_2 = 'modelo_completo.pth'


mean = np.array([0.5, 0.5, 0.5])
std = np.array([0.25, 0.25, 0.25])


Test = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])



model_1 = torch.load(PATH_1)
model_1.eval()

model_2 = torch.load(PATH_2)
model_2.eval()

@csrf_exempt
def predict(file):

  img = Test(Image.open(file))
  batch_img_tensor = torch.unsqueeze(img, 0)  # 0 es el AXIS. 
  out = model_1(batch_img_tensor)
  array = out.detach().numpy()
  
  resultado = array[0][1]
  
  if (resultado > 0.7):
      
      out = model_2(batch_img_tensor)
      array = out.detach().numpy()
      resultado = array[0][1]         #[0][0] es la probabilidad de que sea BENIGNO
      diagnosis = str(resultado*100) + "%"
      mensaje = "Formulario enviado con éxito, la probabilidad de riesgo existente es: " + diagnosis
      return mensaje
    
  else: 
      mensaje = "Esa imagen no parece ser un lunar, por favor intenta tomar una foto con las características mencionadas"
      return mensaje



class post_method(viewsets.ModelViewSet):
    queryset = modelo_imagen.objects.all() #Cada vez que pida una requests van a estar TODOS los objetos puestos en Operacion. 
    serializer_class = imagenserializer #Y usará el OperacionSerializer.

@csrf_exempt
def posteo(request): #En vez de usar el decorador de arriba, que solo servía para POST, este me va a dejar cualquier request.
    
    if request.method == "POST": #Si es un metodo post, arma un form con todos los datos.
        
        form = imagenform(request.POST, request.FILES)
        if form.is_valid():

            data = form.cleaned_data
            imagen = data["imagen"]
            mensaje_final = predict(imagen)

            messages.success(request, mensaje_final)

    else:
        form = imagenform() #Si no es un metodo post, devuelve el coso vacio. 

    return render(request, 'myform/cxform.html', {'form':form})
