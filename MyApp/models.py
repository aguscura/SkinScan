from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class modelo_imagen(models.Model):

    imagen = models.ImageField(upload_to='media')

    def __str__(self):
        return imagen