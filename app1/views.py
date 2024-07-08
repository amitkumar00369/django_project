from django.shortcuts import render
from rest_framework.response import Response
from .models import StudentModel,tokenModel
from .serializer import studentSerializer
from rest_framework import status
import jwt,datetime
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password,make_password
from django.conf import settings
import re
# Create your views here.


class userSingUp(APIView):
    def post(self,request):
        try:
            serializer=studentSerializer(data=request.data)
            print(serializer)
          
            if serializer.is_valid():
                serializer.save()
                
              
                return Response({'message':"Successfull",
                                 'data':serializer.data,
                                 'status':200
                                 
                                 },status.HTTP_200_OK)
                
            else:
                return Response({'message':serializer.errors,'status':400})
        except Exception as e:
            return Response({'message':"Internal server error",'error':str(e.args),'status':500},status=500)

class studentLogin(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            if email is None:
                return Response({'message': "Enter email"}, status=404)
            if password is None:
                return Response({'message': "Enter password"}, status=404)
            
            user = StudentModel.objects.filter(email=email).first()
            
            if not user:
                return Response({'message': "User not found"}, status=404)
            
           
            if not check_password(password, user.password):
          
                return Response({'message': "Please enter correct password"}, status=404)
            
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow()
            }
            
            token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
            
            tokens = tokenModel.objects.filter(email=email).first()
            if not tokens:
                tokenModel.objects.create(userId=user.id, email=user.email, token=token)
            else:
                tokens.token = token
                tokens.save()
            
            # Extract device type from User-Agent header
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
           
            
            if re.search('mobile|android|iphone', user_agent):
                deviceType = 'mobile'
            elif re.search('tablet|ipad', user_agent):
                deviceType = 'tablet'
            else:
                deviceType = 'desktop'
            
            
            
            # Update device type
            # Extract IP address
            # Update device type and IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')

    
            
            user.ipAddress = ip_address
            
            user.deviceType = deviceType
            user.save()
            
            return Response({
                'message': 'Login Successful',
                'email': user.email,
                'token': token,
                'deviceType': user.deviceType,
                'ipAddress':user.ipAddress,
                'status': status.HTTP_200_OK
            }, status=200)
        
        except Exception as e:
          
            return Response({'message': str(e)}, status=500)
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
        except jwt.ExpiredSignatureError:
            return Response('Token has been expired')
        except jwt.InvalidTokenError:
            return Response('Invallid token')
    
        except Exception as e:
            return Response(str(e))
class changePassword(APIView):
    def put(self,request):
        try:
            token=request.headers.get('Authorization')
            if not token:
                return Response({'message':'Token not found','status':status.HTTP_404_NOT_FOUND},status=404)
            decode=jwt.decode(token,settings.JWT_SECRET_KEY,['HS256'])
            userId=decode['id']
            user=StudentModel.objects.filter(id=userId).first()
            if not user:
                return Response({'message':'User not found','status':status.HTTP_404_NOT_FOUND},status=404)
            oldPassword=request.data.get('oldPassword')
            newPassword=request.data.get('newPassword')
            if not oldPassword:
                return Response({'message':'please enter oldPassword','status':status.HTTP_400_BAD_REQUEST},status=400)
            if not newPassword or newPassword is None:
                return Response({'message':'please enter newPassword','status':status.HTTP_400_BAD_REQUEST},status=400)
            if not check_password(oldPassword,user.password):
                return Response({'message':'please enter correct oldPassword','status':status.HTTP_401_UNAUTHORIZED},status=401)
            hashPass=make_password(newPassword)
            user.password=hashPass
            user.save()
            return Response({"message":"User change password succesafully",'email':user.email,'password':newPassword,'status':status.HTTP_200_OK},status=200)
        except jwt.ExpiredSignatureError:
            return ('Token has Expired')
        except jwt.InvalidTokenError:
            return ('Invalid Token')
        except Exception as e:
            return Response({'message':str(e)},status=500)
            
        
                
            
                
        
class getAllUser(APIView):
    def get(self,request):
        try:
            token=request.headers.get('Authorization')
            if not token:
                users=StudentModel.objects.all().order_by('id')
                print('Hello')
                serializer=studentSerializer(users,many=True)
                return Response({'message':"Successfull",'data':serializer.data},status=200)
            else:
                decode=jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=['HS256'])
                userId=decode['id']
                user=StudentModel.objects.filter(id=userId).first()
                serializer=studentSerializer(user)
                if not user:
                    return Response({'message':'User Not found','status':status.HTTP_400_BAD_REQUEST},status=400)
                return Response({'message':'Successfull','data':serializer.data},status=200)
            
                
        except Exception as e:
            return Response({
                'message':str(e)
            },status=500)
            
                
                
     
    
class delete(APIView):
    def delete(self,request):
        user=StudentModel.objects.all()
        user.delete()
        return Response("success")

