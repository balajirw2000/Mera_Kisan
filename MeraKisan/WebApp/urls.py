from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('contact/', views.contact),
    path('DigitalPlatform/', views.DigitalPlatform),
    path('About/', views.About),
    path('add1', views.add1, name='add1'),
    path('ProdAdd/', views.Prodadd, name='Prodadd'),

    path('signup1/', views.aadharveri, name='aadharveri'),
]
