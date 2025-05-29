from django.urls import path
from . import views

urlpatterns = [
    # Main page URL
    path('', views.main_page, name='main_page'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin URLs - Changed from 'admin/' to 'dashboard/'
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/user/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('dashboard/user/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('dashboard/photo/<int:photo_id>/delete/', views.admin_delete_photo, name='admin_delete_photo'),
    
    # Recipe views
    path('recipes/', views.photo_list, name='photo_list'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:recipe_id>/favorite/', views.toggle_favorite_recipe, name='toggle_favorite_recipe'),
    path('recipe/<int:recipe_id>/update/', views.update_recipe, name='update_recipe'),
    path('recipe/<int:recipe_id>/toggle-visibility/', views.toggle_recipe_visibility, name='toggle_recipe_visibility'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('favorites/', views.favorite_photos, name='favorite_photos'),
    path('ingredient/create/', views.create_ingredient, name='create_ingredient'),
] 