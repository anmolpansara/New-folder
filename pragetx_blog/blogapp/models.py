from django.db import models


class trackingData(models.Model):
    campaign=models.CharField(max_length=255,null=True,blank=True,verbose_name='Campaign')
    medium=models.CharField(max_length=255,null=True,blank=True,verbose_name='Medium')
    page=models.CharField(max_length=255,null=True,blank=True,verbose_name='Page')
    ref=models.CharField(max_length=255,null=True,blank=True,verbose_name='Ref')
    source=models.CharField(max_length=255,null=True,blank=True,verbose_name='Source')

    def __str__(self):
            return f"Tracking Data - ID: {self.id}"