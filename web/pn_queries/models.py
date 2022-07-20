from tabnanny import verbose
from django.db import models


class Oo(models.Model):
    oo = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.oo
       
    class Meta:
        db_table = 'oo'
    

class Owner(models.Model):
    owner = models.CharField(max_length=60, unique=True)
    telegram_id = models.CharField(max_length=12, null=True, blank=True)
    
    def __str__(self):
        return self.owner
    
    class Meta:
        db_table = 'owners'


class Service(models.Model):
    service = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.service
    
    class Meta:
        db_table = 'services'
    

class Pn_query(models.Model):
    id_oo = models.ForeignKey(Oo, on_delete=models.PROTECT, verbose_name="Объект обслуживания")
    id_owner = models.ForeignKey(Owner, on_delete=models.PROTECT, verbose_name="Заявитель")
    date_create = models.DateTimeField(verbose_name="Дата создания")
    text = models.TextField(verbose_name="Заявка")
    photo_link = models.FilePathField(path='D:', max_length=160, null=True, blank=True) #debt: create a valid root path
    active = models.BooleanField(default=True)
    date_end = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Ответственные")
    
    def __str__(self):
        return str(self.date_create)[:19]
    
    class Meta:
        db_table = 'pn_queries'
