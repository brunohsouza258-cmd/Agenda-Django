from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# id (primary key - automático)
# first_name (string), last_name (string), phone (string)
# email (email), created_date (date), description (text)
# category (foreign key), show (boolean), picture (imagem)

# Depois
# owner (foreign key)
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'


    name =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=50, verbose_name= 'Primeiro Nome')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Ultimo Nome')
    phone = models.CharField(max_length=50, verbose_name='Telefone')
    email = models.EmailField(max_length=254, blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%M')
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        blank=True, null=True
        )
    owner =  models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        blank=True, null=True
        )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

