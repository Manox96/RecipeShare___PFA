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
    path('dashboard/export-recipes/', views.export_recipe_data, name='export_recipe_data'),
    path('dashboard/backup-users/', views.backup_user_data, name='backup_user_data'),
    path('dashboard/recipe-statistics/', views.recipe_statistics, name='recipe_statistics'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-users/user/<int:user_id>/recipes/', views.admin_user_recipes, name='admin_user_recipes'),
    
    # Recipe views
    path('recipes/', views.photo_list, name='photo_list'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:recipe_id>/favorite/', views.toggle_favorite_recipe, name='toggle_favorite_recipe'),
    path('recipe/<int:recipe_id>/update/', views.update_recipe, name='update_recipe'),
    path('recipe/<int:recipe_id>/toggle-visibility/', views.toggle_recipe_visibility, name='toggle_recipe_visibility'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('recipes/favorites/', views.favorite_photos, name='favorite_photos'),
    path('ingredient/create/', views.create_ingredient, name='create_ingredient'),
    path('tag/create/', views.create_tag, name='create_tag'),
    path('cuisine/<int:cuisine_id>/', views.recipes_by_cuisine, name='recipes_by_cuisine'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/create/', views.create_blog, name='create_blog'),
    path('blog/<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),
    path('blog/<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),
    path('blog/<int:blog_id>/comment/', views.add_blog_comment, name='add_blog_comment'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home, name='home'),
    path('manage/tags/', views.manage_tags, name='manage_tags'),
    path('manage/ingredients/', views.manage_ingredients, name='manage_ingredients'),
    path('manage/tags/<int:tag_id>/update/', views.update_tag, name='update_tag'),
    path('manage/tags/<int:tag_id>/delete/', views.delete_tag, name='delete_tag'),
    path('manage/ingredients/<int:ingredient_id>/update/', views.update_ingredient, name='update_ingredient'),
    path('manage/ingredients/<int:ingredient_id>/delete/', views.delete_ingredient, name='delete_ingredient'),
    path('profile/', views.profile_view, name='profile'),
] 