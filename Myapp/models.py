from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class JsonData(models.Model):
    json_data = models.JSONField(default=dict,null=True,blank=True)
    created = models.DateField(auto_now=True)
    user = models.ForeignKey(User,related_name="json_uploads",on_delete=models.CASCADE)