from rest_framework import serializers
from . models import imagen

class operacionSerializers(serializers.ModelSerializer):
    class MetaData:

        model = imagen
        fields = "__all__" #Importa TODAS los campos de la clase Operacion.

    