from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('tag/<int:pk>/', views.tag_detail, name='tag_detail'),
    path('tag/new/', views.TagCreateView.as_view(), name='tag_new'),
    path('tag/<int:pk>/edit/', views.TagUpdateView.as_view(), name='tag_edit'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('edit-profile/', views.edit_user, name='edit_user'),
    path('tag/<int:tag_id>/direccion/<int:direccion_id>/eliminar/', views.eliminar_direccion, name='eliminar_direccion'),
    path('tag/<int:pk>/delete/', views.tag_delete, name='tag_delete'),
    path('obtener-sectores/<int:empresa_id>/', views.obtener_sectores, name='obtener_sectores'),
    
    
    path('empresas/', views.empresa_list, name='empresa_list'),
    path('empresa/new/', views.empresa_create, name='empresa_create'),
    path('empresa/<int:pk>/edit/', views.empresa_edit, name='empresa_edit'),
    path('empresa/<int:pk>/delete/', views.empresa_delete, name='empresa_delete'),
    
    path('sectores/', views.sector_list, name='sector_list'),
    path('sector/new/', views.sector_create, name='sector_create'),
    path('sector/<int:pk>/edit/', views.sector_edit, name='sector_edit'),
    path('sector/<int:pk>/delete/', views.sector_delete, name='sector_delete'),
    
]