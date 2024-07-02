from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from rest_framework import status
from django.contrib.auth.hashers import make_password,check_password

from rest_framework.response import Response
from .models import StudentsTable,TokenTable
import json
import jwt,datetime
from django.conf import settings

class Register(APIView):
    def post(self,request):
        try:
            email=request.data.get('email')
            name=request.data.get('name')
            password=request.data.get('password')
            mobileNo=request.data.get('mobileNo')
            companyName=request.data.get('companyName')
            IsInd=request.data.get('IsInd')
            elegibilty=request.data.get('elegibilty')
            
            users=StudentsTable.objects.filter(email=email).first()
            if users:
                return Response({'message':"Already user has registerd",'status':status.HTTP_400_BAD_REQUEST},status=400)
                
            
            
            # if not email or not name or not mobileNo or not companyName or not IsInd:
            #     return Response({'message':"Please enter valid fields",'status':status.HTTP_400_BAD_REQUEST},status=400)
            hashPass=make_password(password=password)
            if not hashPass:
                return Response({'message':"password not hashed",'status':status.HTTP_400_BAD_REQUEST},status=400)
                
            user=StudentsTable(email=email,name=name,password=hashPass,mobileNo=mobileNo,companyName=companyName,IsInd=IsInd,elegibilty=elegibilty)
            if not user:
                return Response({'message':"User not registered ",'status':status.HTTP_400_BAD_REQUEST},status=400)
                
            user.save()
            
            student=StudentsTable.objects.filter(email=email).first()
            return Response({'message':"Successfull registered",'details':json.loads(student.to_json())})
        except Exception as e:
            return Response({'msg':str(e)})
class studentLogin(APIView):
    def post(self,request):
        try:
            email=request.data.get('email')
            password=request.data.get('password')
            
            if not email:
                return Response({'message':"please enterd email",'status':status.HTTP_400_BAD_REQUEST},status=400)
            if not password:
                return Response({'message':"please enter password",'status':status.HTTP_400_BAD_REQUEST},status=400)
            user=StudentsTable.objects.filter(email=email).first()
            if not user:
                return Response({'message':"user not found",'status':status.HTTP_400_BAD_REQUEST},status=400)
            if not check_password(password,user.password):
                return Response({'message':"password not macthed",'status':status.HTTP_400_BAD_REQUEST},status=400)
           
            payload={
                # 'id':user._id,
                'email':user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat':datetime.datetime.utcnow()
            }
            token=jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
        
            find=TokenTable.objects.filter(email=email).first()
        
           
            if not find:
               
                tokens=TokenTable.objects.create(email=email,token=token)
            else:
                find.token=token
                find.save()
            
            return Response({'msg':"Successful Login",'email':user.email,'token':token},status=200)
        except Exception as e:
            return Response(str(e))
    
        
                
                
        
    
class allStudents(APIView):
    def get(self,request,email=None):
        try:
            if email is None:
                student=StudentsTable.objects.all()
                if not student:
                    return Response({'message':"students not found ",'status':status.HTTP_404_NOT_FOUND},status=404)
            else:
                student=StudentsTable.objects.filter(email=email).first()
                if student is None:
                    
                    return Response({'message':"student not found ",'status':status.HTTP_404_NOT_FOUND},status=404)
                
            return Response({'msg':'Successfull','data':json.loads(student.to_json()),'status':status.HTTP_200_OK},status=200)
        except Exception as e:
            return Response(str(e))
        
class changePassword(APIView):
    def post(self,request):
        try:
            token=request.headers.get('Authorization')
            if not token:
                return Response({'message':"token not found ",'status':status.HTTP_404_NOT_FOUND},status=404)
          
            decode=jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
           
            if not decode:
                return Response({'message':"token not verify ",'status':status.HTTP_400_BAD_REQUEST},status=400)
            
            oldPass=request.data.get('oldPassword')
            newPass=request.data.get('newPassword')
            if not oldPass:
                return Response({'message':"please enter old password",'status':status.HTTP_400_BAD_REQUEST},status=400)
            if not newPass:
                return Response({'message':"please enter new password",'status':status.HTTP_400_BAD_REQUEST},status=400)
             
            email=decode['email']
            user=StudentsTable.objects.filter(email=email).first()
            # tokens=TokenTable.objects.filter(email=user.email).first()
            # print(tokens)
            if not user :
                return Response({'message':"student not found ",'status':status.HTTP_404_NOT_FOUND},status=404)
            if not check_password(oldPass,user.password):
                return Response({'message':"please enter correct old password ! ",'status':status.HTTP_400_BAD_REQUEST},status=400)
            
            user.password=make_password(newPass)
            user.save()
            return Response({'msg':'Password changed successfully','email':decode['email'],'newPassword':newPass},status=200)
        except Exception as e:
            return Response(str(e))
        
class studentLogout(APIView):
    def post(self,request):
        try:
            token=request.headers.get('Authorization')
            if not token:
                return Response({'message':"token not found ",'status':status.HTTP_404_NOT_FOUND},status=404)
          
            decode=jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            
            if not decode:
                return Response({'message':"token not verify ",'status':status.HTTP_400_BAD_REQUEST},status=400)
            email=decode['email']
            tokens=TokenTable.objects.filter(email=email).all()
            if not tokens:
                return Response({'message':'Student already logout','status':status.HTTP_200_OK},status=200)
            tokens.delete()
            return Response({'message':'Student logout successdully','email':email},status=200)
        except Exception as e:
            return Response(str(e))
                
                