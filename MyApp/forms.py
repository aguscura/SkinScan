from django import forms
from . models import modelo_imagen

class imagenform(forms.ModelForm):

    class Meta:
        model = modelo_imagen
        fields = ['imagen',]

    def __init__(self, *args, **kwargs):
        super(imagenform, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = True