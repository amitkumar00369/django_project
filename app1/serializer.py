from rest_framework import serializers

from .models import StudentModel
class studentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=StudentModel
        fields=['id','name','email','mobileNo','password','countryName','countryCode']