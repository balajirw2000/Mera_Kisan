from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Addproducts(models.Model):
     id = models.AutoField(primary_key=True)
     username= models.CharField(max_length=100)
     product_name= models.CharField(max_length=100)
     product_variety = models.CharField(max_length=100)
     quantity = models.CharField(max_length=100)
     value = models.CharField(max_length=100)
     city_name = models.CharField(max_length=100)
     section = models.CharField(max_length=100)
     price = models.CharField(max_length=100)
     price_value= models.CharField(max_length=100)
     image=models.ImageField(upload_to='pics')

class Orders(models.Model):
     #user = models.OneToOneField(User, on_delete=models.CASCADE)
     order_id= models.AutoField(primary_key=True)
     items_json= models.CharField(max_length=5000)
     amount = models.IntegerField(default=0)
     name=models.CharField(max_length=90)
     email=models.CharField(max_length=111)
     address=models.CharField(max_length=500)
     city=models.CharField(max_length=111)
     state=models.CharField(max_length=111)
     zip_code=models.CharField(max_length=111)
     phone =models.CharField(max_length=14,default="")

class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(default=now)
    def __str__(self):
         return self.update_desc[0:7] + "..."



class AddComments(models.Model):
     com_id = models.AutoField(primary_key=True)
     pr_id = models.IntegerField()
     comment = models.TextField()
     reply_id = models.IntegerField(blank=True,default=0)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     product = models.ForeignKey(Addproducts, on_delete=models.CASCADE)
     #parent = models.ForeignKey('self', on_delete=models.CASCADE, default="", blank=True)
     timestamp = models.DateTimeField(default=now)

class Reply(models.Model):
     re_id = models.AutoField(primary_key=True)
     pr_id = models.IntegerField(blank=True)
     reply_id = models.IntegerField(default=0,blank=True)
     comment = models.TextField()
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     product = models.ForeignKey(Addproducts, on_delete=models.CASCADE)
     #parent = models.ForeignKey(Com , on_delete=models.CASCADE, blank=True,null=True)
     timestamp = models.DateTimeField(default=now)