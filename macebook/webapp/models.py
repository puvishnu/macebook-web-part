from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your models here.
class Picture(models.Model):
   picid =  models.AutoField(6,primary_key=True)
   profilefield = models.ImageField(upload_to='static/photo/',null=True,blank=True)
   def save(self, *args, **kwargs):
      super().save(*args, **kwargs)
      img = Image.open(self.profilefield.path)
      output_size = (100, 128)
      img.thumbnail(output_size)
      img.save(self.profilefield.path)

class Department(models.Model):   
   dep=models.CharField(max_length = 40)
   deptid =  models.AutoField(6,primary_key=True)


class Staff(models.Model):
   stafftype=models.CharField(max_length = 40)
   staffid =  models.AutoField(6,primary_key=True)

class Usersreal(models.Model):
   user_id =  models.AutoField(6,primary_key=True)
   name=models.CharField(max_length = 50)
   email=models.CharField(max_length = 50)
   phonenumber = models.CharField(max_length = 20)
   landnumber = models.CharField(max_length = 20)
   password=models.CharField(max_length = 50)
   pic =  models.ForeignKey(Picture,related_name='pictures',on_delete=models.CASCADE,default=17)
   dept = models.ForeignKey(Department,related_name='depts',on_delete=models.CASCADE)
   staff = models.ForeignKey(Staff,related_name='staffs',on_delete=models.CASCADE,)
   is_valid=models.IntegerField(6,default=0)
   is_admin=models.IntegerField(6,default=0)
   is_activate=models.IntegerField(6,default=0)
   

