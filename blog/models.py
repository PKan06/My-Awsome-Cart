from django.db import models
from django.utils import timezone
# Create your models here.

class Blogpost (models.Model):
    post_id = models.AutoField(primary_key=True) #auto incremented key {as primary key is not st so it will make an idkey as id}
    title = models.CharField(max_length=50)  # assuming that product name will not go more than 50 length
    topic = models.CharField(max_length=20,default= "")  
    head0 = models.CharField(max_length=500,default="")
    chead0 = models.CharField(max_length=5000,default="")
    head1 = models.CharField(max_length=500,default="")
    chead1 = models.CharField(max_length=5000,default="")
    head2 = models.CharField(max_length=500,default="")
    chead2 = models.CharField(max_length=5000,default="")   
    pub_date = models.DateField(default=timezone.now) 
    thumnbnaile = models.ImageField(upload_to = 'shop/images',default = "")

    def __str__(self):
        return self.title