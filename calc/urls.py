from django.urls import path
from . import views
urlpatterns = [
    path('',views.login,name='login'),
    path('home',views.home,name='home'),
    path('dataset',views.dataset_creator, name='dataset'),
    path('trainer',views.trainer,name='trainer'),
    path('detect',views.detector,name='detect'),
    path('login',views.login,name='login'),
    path('individual',views.individual,name='individual'),
    path('signup',views.signup,name='signup'),
    path('register',views.register,name='register'),
]