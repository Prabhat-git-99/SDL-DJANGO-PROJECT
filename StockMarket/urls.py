from django.urls import path
from . import views

urlpatterns = [
    path('',views.start,name = 'start'),
    path('pretool.html',views.tool,name = 'tool'),
    path('topgainer.html',views.Gainer,name = 'gainer'),
    path('toploser.html',views.Loser,name = 'loser'),
    path('home.html',views.start,name= 'start'),
    path('mostactive.html',views.active,name = 'start'),
    path('globalmarket.html',views.reccommendation,name = 'reccommendation'),
    path('input',views.input,name = 'input'),
    path('result.html',views.result,name = 'result'),
]