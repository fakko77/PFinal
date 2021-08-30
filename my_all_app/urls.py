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
        path('accounts/login/', views.view_login, name='login'),
        path('edit/', views.edit_password, name='edit'),
        path('accounts/signup/', views.signup, name='signup'),
        path('deleteIndex/<int:indexId>/', views.index_delete, name='deleteIndex'),
        path('deleteIndicator/<int:indicatorId>/', views.indicator_delete, name='deleteIndicator'),
        path('deletePosition/<int:positionId>/', views.position_delete, name='deletePosition'),
        path('positionWin/<int:positionId>/', views.position_win, name='winPosition'),
        path('positionDefeat/<int:positionId>/', views.position_defeat, name='defeatPosition'),

]
