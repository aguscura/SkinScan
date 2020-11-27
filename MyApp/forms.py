from django import forms
from . models import imagen

class operacionform(forms.ModelForm):

    class Meta:

        model = imagen
        fields = ['imagen',]

    def __init__(self, *args, **kwargs):
        super(operacionform, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = False