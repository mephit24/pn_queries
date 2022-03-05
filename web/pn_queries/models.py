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
    id_oo = models.ForeignKey(Oo, on_delete=models.PROTECT)
    id_owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    date_create = models.DateTimeField()
    text = models.TextField()
    photo_link = models.FilePathField(path='', max_length=160, null=True, blank=True) #debt: create a valid root path
    active = models.BooleanField(default=True)
    date_end = models.DateTimeField()
    comment = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True)
    
    class Meta:
        db_table = 'pn_queries'
