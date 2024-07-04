from .views import userSingUp,delete,studentLogin,userLogout,getAllUser


from django.urls import path



urlpatterns = [
    path('userSignUp',userSingUp.as_view()),
    path('delete',delete.as_view()),
    path('userLogin',studentLogin.as_view()),
    path('userLogout',userLogout.as_view()),
    path('getAllUser',getAllUser.as_view())
    
]
