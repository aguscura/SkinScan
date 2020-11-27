from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#La data que va a postear o a pedir. Es la Imagen o el File con la respuesta acerca de la pred ?
#Porque yo tengo dos tipos de datos. Posteo imagenes, recibo respuesta escrita.
class MyAccountManager(BaseUserManager):

    def create_user(self,email,username,password=None): #Si o si le tengo q pasar como minimo las variables q están en REQUIRED_FIELDS abajo. 
        
        if not email:
            raise ValueError("Los usuarios deben tener una dirección de mail")
        if not username:
            raise ValueError("Los usuarios deben tener un usuario")

        user = self.model( email=self.normalize_email(email), username = username)

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self,email,username, password):
        
        user = self.create_user(
            
                email = self.normalize_email(email), #Lo que hace es pasar a minuscula toda la direc de mail.
                password = password,
                username = username
                )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
    
        user.save(using=self._db)
        
        return user

        

class Account(AbstractBaseUser):

    email = models.EmailField(verbose_name="email", unique=True, max_length=60)
    username = models.CharField(unique=True, max_length=25)
    date_joined = models.DateTimeField(verbose_name="Fecha de Entrada", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Ultimo Login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']   #Para registrarse 

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class imagen(models.Model):

    imagen = models.ImageField(upload_to='Imagenes')

    def __str__(self):
        return imagen