from django.urls import path
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
        path('calculator/', views.calculator, name='calculator'),
        path('add/', views.add, name='add'),
        path('manage/', views.manage, name='manage'),
        path('history/', views.history, name='history'),
        path('setting/', views.setting, name='setting'),
        path('login/', views.view_login, name='login'),
        path('deleteIndex/<int:indexId>/', views.indexDelete, name='deleteIndex'),
        path('deleteIndicator/<int:indicatorId>/', views.IndicatorDelete, name='deleteIndicator'),
        path('deletePosition/<int:positionId>/', views.positionDelete, name='deletePostion'),
        path('positionWin/<int:positionId>/', views.positionWin, name='winPostion'),
        path('positionDefeat/<int:positionId>/', views.positionDefeat, name='defeatPostion'),





]
