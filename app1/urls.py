from .views import userSingUp,delete,studentLogin,userLogout


from django.urls import path



urlpatterns = [
    path('userSignUp',userSingUp.as_view()),
    path('delete',delete.as_view()),
    path('userLogin',studentLogin.as_view()),
    path('userLogout',userLogout.as_view())
    
]
