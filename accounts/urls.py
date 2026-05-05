from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',    auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/',   auth_views.LogoutView.as_view(), name='logout'),
    path('usuarios/', views.user_list,   name='user_list'),
    path('usuarios/nuevo/', views.user_create, name='user_create'),
    path('usuarios/<int:pk>/editar/', views.user_edit, name='user_edit'),
    path('usuarios/<int:pk>/toggle/', views.user_toggle, name='user_toggle'),
]
