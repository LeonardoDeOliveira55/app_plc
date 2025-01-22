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
]