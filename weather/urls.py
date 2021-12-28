from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='index'),  #the path for our index view
]