from django.db import models

# Create your models here.
from mongoengine import Document, StringField, EmailField,BooleanField

class StudentsTable(Document):
    email = EmailField(required=True)
    name = StringField(max_length=100, required=True)
    mobileNo = StringField(max_length=15,required=True)
    password=StringField(required=True)
    companyName=StringField(max_length=50,required=True)
    IsInd = BooleanField(default=False)
    elegibilty=StringField(max_length=50,required=True)
    
#    user=StudentsTable(email=email,)

class TokenTable(Document):
    email = EmailField(required=True)
    token=StringField(required=True)
    
    
