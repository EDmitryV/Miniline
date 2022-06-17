from django.urls import path
from . import views

boosts = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

lonely_boost = views.BoostViewSet.as_view({
    'put': 'partial_update'
})

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('', views.index, name='index'),
    path('game', views.game, name='game'),
    path('call_click/', views.call_click),
    path('boosts/', boosts, name='boosts'),
    path('boost/<int:pk>/', lonely_boost, name='boost'),
    path('update_points/', views.update_points),
    path('core/', views.get_core),
    path('set_words/', views.set_words_set),
    path('switch_lang/', views.switch_lang),
    path('switch_theme/', views.switch_theme),
    path('get_theme/', views.get_theme)
]
