from django.shortcuts import render
from rest_framework.response import Response
from .models import StudentModel,tokenModel
from .serializer import studentSerializer
from rest_framework import status
import jwt,datetime
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.conf import settings

# Create your views here.


class userSingUp(APIView):
    def post(self,request):
        try:
            serializer=studentSerializer(data=request.data)
            if serializer.is_valid():
                user=serializer.save()
                return Response({'message':"Successfull",
                                 'data':serializer.data,
                                 'status':200
                                 
                                 },status.HTTP_200_OK)
                
            else:
                return Response({'message':serializer.errors,'status':400})
        except Exception as e:
            return Response({'message':"Internal server error",'error':str(e),'status':500},status=500)
        
        
class studentLogin(APIView):
    def post(self,request):
        try:
            email=request.data.get('email')
            password=request.data.get('password')
            if email is None:
                return Response({'message':"enter email"},status=404)
            if password is None:
                
                return Response({'message':"enter password"},status=404)
            
            user=StudentModel.objects.filter(email=email).first()
            if not user:
                return Response({'message':"user not found"},status=404)
            if not check_password(password,user.password):
                return Response({'message':"please enter corroct password"},status=404)
            payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                    'iat': datetime.datetime.utcnow()
                }
            
            token=jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
            print(token)
            tokens=tokenModel.objects.filter(email=email).first()
            if not tokens:
                tokenModel.objects.create(userId=user.id,email=user.email,token=token)
            tokens.token=token
            tokens.save()
            
            return Response({'message':'Login Successfull','email':user.email,'token':token,'status':status.HTTP_200_OK},status=200)
        except Exception as e:
            return Response({'message':str(e)})
        
        
class userLogout(APIView):
    def post(self,request):
        try:
            token=request.headers.get('Authorization')
            if not token:
                return Response({'message':'Token not found !','status':status.HTTP_404_NOT_FOUND},status=404)
            decode=jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=['HS256'])
            print(decode)
            if not decode:
                return Response({'message':'Token not verified !','status':status.HTTP_400_BAD_REQUEST},status=400)
            userId=decode['id']
            tokens=tokenModel.objects.filter(userId=userId).all()
            if not tokens:
                return Response({'message':'User already logout','status':status.HTTP_200_OK},status=200)
            
                
            tokens.delete()
            return Response({'message':'User logout successdully'},status=200)
        except Exception as e:
            return Response(str(e))
    
            
            
                
                
     
    
class delete(APIView):
    def delete(self,request):
        user=StudentModel.objects.all()
        user.delete()
        return Response("success")
        
