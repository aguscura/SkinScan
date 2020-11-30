from rest_framework import serializers
from . models import modelo_imagen

class imagenserializer(serializers.ModelSerializer):
    class MetaData:

        model = modelo_imagen
        fields = "__all__" #Importa TODAS los campos de la clase Operacion.

    