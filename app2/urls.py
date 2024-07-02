from django.urls import path

from .views import Register,allStudents,studentLogin,changePassword,studentLogout
urlpatterns = [
    path('register',Register.as_view()),
    path('all/<str:email>',allStudents.as_view()),
    path('all/',allStudents.as_view()),
    path('studentLogin',studentLogin.as_view()),
    path('changePassword',changePassword.as_view()),
    path('studentLogout',studentLogout.as_view())
]
