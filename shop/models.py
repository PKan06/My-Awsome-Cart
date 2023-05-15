from django.db import models
from django.db.models.fields import AutoField, CharField, IntegerField

# Create your models here.
class Product (models.Model):
    product_id = models.AutoField  #auto incremented key {as primary key is not st so it will make an idkey as id}
    product_name = models.CharField(max_length=50,default="")  # assuming that product name will not go more than 50 length
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0) # default shows that no field is enterd
    desc = models.CharField(max_length=300) # Assuming that the description will of 300 length
    pub_date = models.DateField() 
    image = models.ImageField(upload_to = 'shop/images',default = "")

    def __str__(self):
        return self.product_name


class Contact (models.Model):
    msg_id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=50,default="") 
    email = models.CharField(max_length=70,default="")
    phone = models.CharField(max_length=70,default="")
    desc = models.CharField(max_length=700,default="") 

    def __str__(self):
        return self.name

class Orders (models.Model):
    order_id = models.AutoField(primary_key=True) 
    item_json = models.CharField(max_length=5000,default="")  
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=5000,default="") 
    email = models.EmailField(max_length=5000,default="") 
    address = models.CharField(max_length=2000,default="")
    city = models.CharField(max_length=70,default="")
    state = models.CharField(max_length=700,default="") 
    Zip_code = models.CharField(max_length=20,default="")
    Phone_No = models.CharField(max_length=20,default="")

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key = True)
    order_id = models.IntegerField(default = "")
    update_desc = models.CharField(max_length = 5000)
    timestamp = models.DateField(auto_now_add = True) 

    def __str__(self):
        return self.update_desc[0:7] + "..."

# auto_now_add will assume the current time stamp if no value is given