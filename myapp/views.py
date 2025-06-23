from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import Photo, Recipe, Difficulty, Cuisine, MealType, Ingredient, Unit, RecipeIngredient, Step, Favorite, Tag, Blog
from .forms import PhotoUploadForm, RecipeForm, RecipeIngredientFormSet, StepFormSet, BlogForm, ContactForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count
import datetime
import pycountry
import country_converter as coco
from django.db.models import Q

# Home view with integrated upload form
@login_required(login_url='login')
def home(request):
    # Handle form submission
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, 'Photo uploadée avec succès !')
            return redirect('home')
    else:
        form = PhotoUploadForm()
        
    # Get photos for display
    photos = Photo.objects.filter(user=request.user).order_by('-upload_date')
    favorites_count = Photo.objects.filter(favorites=request.user).count()
    
    context = {
        'title': 'Accueil',
        'photos': photos,
        'form': form,
        'favorites_count': favorites_count,
    }
    return render(request, 'myapp/photo_list.html', context)

def main_page(request):
    meal_type_id = request.GET.get('meal_type')
    recipes = Recipe.objects.filter(is_public=True).order_by('-created_at')
    meal_types = MealType.objects.all()
    
    # Annotate cuisines with recipe count and flag emoji
    cuisines = Cuisine.objects.annotate(recipe_count=Count('recipe')).filter(recipe_count__gt=0)
    
    # Helper to get flag emoji from country code
    def country_code_to_emoji(code):
        if not code or len(code) != 2:
            return "🌎"
        return chr(0x1F1E6 + ord(code.upper()[0]) - ord('A')) + chr(0x1F1E6 + ord(code.upper()[1]) - ord('A'))
    for cuisine in cuisines:
        cuisine.flag_emoji = country_code_to_emoji(cuisine.country_code) if cuisine.country_code else "🌎"

    if meal_type_id:
        recipes = recipes.filter(meal_type_id=meal_type_id)

    paginator = Paginator(recipes, 3)  # Show 3 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_user_favorite = []
    if request.user.is_authenticated:
        all_user_favorite = request.user.favorite_set.all().values_list('recipe_id', flat=True)

    # Additional context for new homepage sections
    categories = Tag.objects.all()
    popular_recipes = Recipe.objects.filter(is_public=True).order_by('-created_at')[:4]
    
    # Get newly added recipes (last 3 days)
    three_days_ago = timezone.now() - datetime.timedelta(days=300)
    new_recipes = Recipe.objects.filter(is_public=True, created_at__gte=three_days_ago).order_by('-created_at')
    
    cooking_tips = [
        "Always taste as you cook.",
        "Let meat rest before slicing.",
        "Use fresh herbs for better flavor.",
        "Read the recipe all the way through before starting.",
    ]

    # Get 2 random blog posts
    random_blogs = Blog.objects.order_by('?')[:2]

    context = {
        'title': 'Welcome to Recipe Share',
        'recipes': page_obj,
        'is_public': True,
        'meal_types': meal_types,
        'selected_meal_type': int(meal_type_id) if meal_type_id else None,
        'categories': categories,
        'popular_recipes': popular_recipes,
        'new_recipes': new_recipes,
        'cooking_tips': cooking_tips,
        'cuisines': cuisines,
        'random_blogs': random_blogs,
        'all_user_favorite': all_user_favorite,
    }
    
    return render(request, 'myapp/main_page.html', context)

# Photo list view - modified to allow public access
@login_required(login_url='login')
def photo_list(request):
    # Fetch all recipes for the current user
    recipes = Recipe.objects.filter(user=request.user).order_by('-created_at')

    # Get all favorite recipe IDs for the current user
    all_user_favorite = request.user.favorite_set.all().values_list('recipe_id', flat=True)

    # Count favorite recipes for the current user
    favorites_count = all_user_favorite.count()

    # Add pagination
    paginator = Paginator(recipes, 9)  # Show 9 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'all_user_favorite' : all_user_favorite,  # Pass the list of favorite recipe IDs
        'recipes': page_obj,  # Pass the page object instead of the queryset
        'favorites_count': favorites_count,
        'is_public': False, # This view is for logged-in users' recipes
        'title': 'My Recipes',
    }
    return render(request, 'myapp/photo_list.html', context)

# Photo detail view
@login_required(login_url='login')
def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    photos = Photo.objects.all().order_by('-upload_date')
    context = {
        'photo': photo,
        'photos': photos,
    }
    return render(request, 'myapp/photo_detail.html', context)

# Class-based photo detail view
class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'myapp/photo_detail.html'
    context_object_name = 'photo'

# Photo upload view
@login_required(login_url='login')
def upload_photo(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = RecipeIngredientFormSet(request.POST, prefix='ingredients')
        step_formset = StepFormSet(request.POST, prefix='steps')
        
        # First validate the main form
        if form.is_valid():
            try:
                # Create the recipe first
                recipe = form.save(commit=False)
                recipe.user = request.user
                recipe.save()
                form.save_m2m()  # Save tags
                
                # Now validate and save ingredients
                ingredient_formset.instance = recipe
                if ingredient_formset.is_valid():
                    ingredient_formset.save()
                else:
                    recipe.delete()  # Clean up if ingredients are invalid
                    for error in ingredient_formset.non_form_errors():
                        messages.error(request, f'Ingredient error: {error}')
                    for form in ingredient_formset.forms:
                        for field, errors in form.errors.items():
                            for error in errors:
                                messages.error(request, f'Ingredient {form.instance.id or "new"}: {field} - {error}')
                    return render(request, 'myapp/upload_photo.html', {
                        'form': form,
                        'ingredient_formset': ingredient_formset,
                        'step_formset': step_formset,
                        'difficulties': Difficulty.objects.all(),
                        'cuisines': Cuisine.objects.all(),
                        'meal_types': MealType.objects.all(),
                        'ingredients': Ingredient.objects.all(),
                        'units': Unit.objects.all(),
                        'tags': Tag.objects.all(),
                    })
                
                # Finally validate and save steps
                step_formset.instance = recipe
                if step_formset.is_valid():
                    step_formset.save()
                    messages.success(request, 'Recipe created successfully!')
                    return redirect('photo_list')
                else:
                    recipe.delete()  # Clean up if steps are invalid
                    for error in step_formset.non_form_errors():
                        messages.error(request, f'Step error: {error}')
                    for form in step_formset.forms:
                        for field, errors in form.errors.items():
                            for error in errors:
                                messages.error(request, f'Step {form.instance.id or "new"}: {field} - {error}')
                    return render(request, 'myapp/upload_photo.html', {
                        'form': form,
                        'ingredient_formset': ingredient_formset,
                        'step_formset': step_formset,
                        'difficulties': Difficulty.objects.all(),
                        'cuisines': Cuisine.objects.all(),
                        'meal_types': MealType.objects.all(),
                        'ingredients': Ingredient.objects.all(),
                        'units': Unit.objects.all(),
                        'tags': Tag.objects.all(),
                    })
            except Exception as e:
                messages.error(request, f'Error saving recipe: {str(e)}')
        else:
            # Show form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RecipeForm()
        ingredient_formset = RecipeIngredientFormSet(prefix='ingredients')
        step_formset = StepFormSet(prefix='steps')
    
    # Get all the necessary data for dropdowns
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'difficulties': Difficulty.objects.all(),
        'cuisines': Cuisine.objects.all(),
        'meal_types': MealType.objects.all(),
        'ingredients': Ingredient.objects.all(),
        'units': Unit.objects.all(),
        'tags': Tag.objects.all(),
        'title': 'Upload New Recipe',  # Add title to context
    }
    return render(request, 'myapp/upload_photo.html', context)

@login_required(login_url='login')
def toggle_favorite(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.user in photo.favorites.all():
        photo.favorites.remove(request.user)
    else:
        photo.favorites.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'photo_list'))

def login_view(request):
    # If user is already logged in, redirect to photo list
    if request.user.is_authenticated:
        return redirect('photo_list')
        
    next_url = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type', 'user')
        # Use next from POST if available
        next_url = request.POST.get('next') or next_url
        if not next_url:
            referer = request.META.get('HTTP_REFERER')
            if referer and '/login' not in referer:
                next_url = referer
            else:
                next_url = 'photo_list'
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is admin when admin login is selected
            if login_type == 'admin' and not user.is_staff:
                messages.error(request, 'This account does not have admin privileges.')
                return render(request, 'myapp/login.html')
            
            login(request, user)
            messages.success(request, f'Welcome back{" admin" if login_type == "admin" else ""}!')
            
            # Redirect admin users to admin dashboard
            if login_type == 'admin':
                return redirect('admin_dashboard')
            
            # Redirect to next_url
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        if not next_url:
            referer = request.META.get('HTTP_REFERER')
            if referer and '/login' not in referer:
                next_url = referer
            else:
                next_url = 'photo_list'
    return render(request, 'myapp/login.html')

def register_view(request):
    # If user is already logged in, redirect to photo list
    if request.user.is_authenticated:
        return redirect('photo_list')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'myapp/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'myapp/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'myapp/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('photo_list')
    
    return render(request, 'myapp/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required(login_url='login')
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.method == 'POST':
        # Clear all favorites before deleting the photo
        photo.favorites.clear()
        photo.delete()
        messages.success(request, 'Photo supprimée avec succès !')
        return redirect('photo_list')
    return redirect('photo_detail', photo_id=photo_id)

@login_required(login_url='login')
def favorite_photos(request):
    # Get all recipes that the user has favorited
    recipes = Recipe.objects.filter(favorite__user=request.user).order_by('-created_at')
    favorites_count = recipes.count()

    # Get all favorite recipe IDs to pass to template
    all_user_favorite = recipes.values_list('id', flat=True)
    
    # Add pagination
    paginator = Paginator(recipes, 9)  # Show 9 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'all_user_favorite': all_user_favorite,
        'recipes': page_obj,
        'title': 'Saved Recipes',
        'favorites_count': favorites_count,
        'is_public': False,
    }
    return render(request, 'myapp/photo_list.html', context)

@login_required(login_url='login')
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Ensure the user is the owner of the recipe before updating
    if request.user != recipe.user:
        messages.error(request, 'You do not have permission to update this recipe.')
        return redirect('recipe_detail', recipe_id=recipe_id)
        
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(request.POST, instance=recipe, prefix='steps')
        
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            form.save()
            ingredient_formset.save()
            step_formset.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipe_detail', recipe_id=recipe.id)
        else:
            # Add form and formset errors to the context
            context = {
                'form': form,
                'recipe': recipe,
                'ingredient_formset': ingredient_formset,
                'step_formset': step_formset,
                'difficulties': Difficulty.objects.all(),
                'cuisines': Cuisine.objects.all(),
                'meal_types': MealType.objects.all(),
                'ingredients': Ingredient.objects.all(),
                'units': Unit.objects.all(),
                'title': f'Update {recipe.title}'
            }
            # Manually add formset errors to messages for visibility
            if not ingredient_formset.is_valid():
                for formset_form in ingredient_formset:
                    for field, errors in formset_form.errors.items():
                        for error in errors:
                            messages.error(request, f'Ingredient - {field}: {error}')
                for error in ingredient_formset.non_form_errors():
                     messages.error(request, f'Ingredient (General): {error}')
            if not step_formset.is_valid():
                 for formset_form in step_formset:
                    for field, errors in formset_form.errors.items():
                        for error in errors:
                            messages.error(request, f'Step - {field}: {error}')
                 for error in step_formset.non_form_errors():
                     messages.error(request, f'Step (General): {error}')
            return render(request, 'myapp/update_recipe.html', context)
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(instance=recipe, prefix='steps')
    
    context = {
        'form': form,
        'recipe': recipe,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'difficulties': Difficulty.objects.all(),
        'cuisines': Cuisine.objects.all(),
        'meal_types': MealType.objects.all(),
        'ingredients': Ingredient.objects.all(),
        'units': Unit.objects.all(),
        'title': f'Update {recipe.title}'
    }
    return render(request, 'myapp/update_recipe.html', context)

def is_admin(user):
    return user.is_staff

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') == 'on'
        is_active = 'is_active' in request.POST
        
        # Check if username is already taken by another user
        if User.objects.exclude(id=user_id).filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'myapp/admin_edit_user.html', {'user': user})
        
        # Check if email is already taken by another user
        if User.objects.exclude(id=user_id).filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'myapp/admin_edit_user.html', {'user': user})
        
        user.username = username
        user.email = email
        user.is_staff = is_staff
        user.is_active = is_active
        
        if password:
            user.set_password(password)
        
        user.save()
        messages.success(request, f'User {user.username} updated successfully.')
        return redirect('manage_users')
    
    return render(request, 'myapp/admin_edit_user.html', {'user': user})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Prevent deleting the last admin
    if user.is_staff and User.objects.filter(is_staff=True).count() <= 1:
        messages.error(request, 'Cannot delete the last admin user.')
        return redirect('admin_dashboard')
    
    # Prevent deleting yourself
    if user == request.user:
        messages.error(request, 'Cannot delete your own account.')
        return redirect('admin_dashboard')
    
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('admin_dashboard')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    photo.delete()
    messages.success(request, 'Photo deleted successfully!')
    return redirect('admin_dashboard')

# Recipe detail view
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    # You might want to fetch related ingredients and steps here if not already accessible via recipe object
    context = {
        'recipe': recipe,
        'title': recipe.title,
    }
    return render(request, 'myapp/recipe_detail.html', context)

@login_required(login_url='login')
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    # Ensure the user is the owner of the recipe before deleting
    if request.user == recipe.user:
        if request.method == 'POST':
            recipe.delete()
            messages.success(request, 'Recipe deleted successfully!')
            return redirect('photo_list') # Redirect to the recipe list after deletion
        else:
             # Optionally show a confirmation page if not a POST request
             pass # For now, just handle POST delete
    else:
        messages.error(request, 'You do not have permission to delete this recipe.')
        return redirect('recipe_detail', recipe_id=recipe_id) # Redirect back to recipe detail 

@login_required(login_url='login')
def toggle_favorite_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    # Check if a Favorite object exists for this user and recipe
    favorite_exists = Favorite.objects.filter(user=request.user, recipe=recipe).exists()

    if favorite_exists:
        # If it exists, remove it
        Favorite.objects.filter(user=request.user, recipe=recipe).delete()
        messages.success(request, 'Recipe removed from favorites.')
    else:
        # If it doesn't exist, create it
        Favorite.objects.create(user=request.user, recipe=recipe)
        messages.success(request, 'Recipe added to favorites.')

    # Redirect back to the previous page or a default if no referer
    return redirect(request.META.get('HTTP_REFERER', 'photo_list'))

@login_required(login_url='login')
def toggle_recipe_visibility(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    # Ensure the user is the owner of the recipe
    if request.user == recipe.user:
        recipe.is_public = not recipe.is_public
        recipe.save()
        messages.success(request, f'Recipe is now {"public" if recipe.is_public else "private"}!')
    else:
        messages.error(request, 'You do not have permission to modify this recipe.')
    return redirect(request.META.get('HTTP_REFERER', 'photo_list'))

@login_required(login_url='login')
def create_ingredient(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            try:
                # Check if ingredient already exists (case-insensitive)
                ingredient, created = Ingredient.objects.get_or_create(name__iexact=name, defaults={'name': name})
                if created:
                    response_data = {
                        'success': True,
                        'message': f'Ingredient "{name}" created successfully!',
                        'ingredient': {
                            'id': ingredient.id,
                            'name': ingredient.name
                        }
                    }
                else:
                    response_data = {
                        'success': False,
                        'message': f'Ingredient "{name}" already exists!',
                        'ingredient': {
                            'id': ingredient.id,
                            'name': ingredient.name
                        }
                    }
                return JsonResponse(response_data)
            except Exception as e:
                error_message = f'Error creating ingredient: {str(e)}'
                return JsonResponse({
                    'success': False,
                    'message': error_message
                }, status=400)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Ingredient name is required.'
            }, status=400)
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)

@login_required(login_url='login')
def create_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            try:
                tag, created = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
                if created:
                    response_data = {
                        'success': True,
                        'tag': {
                            'id': tag.id,
                            'name': tag.name
                        }
                    }
                else:
                    response_data = {
                        'success': False,
                        'message': f'Tag "{name}" already exists!'
                    }
                return JsonResponse(response_data)
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error creating tag: {str(e)}'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Tag name is required.'}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

def recipes_by_cuisine(request, cuisine_id):
    from django.core.paginator import Paginator
    cuisine = get_object_or_404(Cuisine, id=cuisine_id)
    recipes = Recipe.objects.filter(is_public=True, cuisine=cuisine).order_by('-created_at')
    paginator = Paginator(recipes, 9)  # Show 9 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'cuisine': cuisine,
        'recipes': page_obj,
        'title': f"{cuisine.name} Recipes",
    }
    return render(request, 'myapp/recipes_by_cuisine.html', context)

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    context = {
        'blogs': blogs,
        'title': 'Blog'
    }
    return render(request, 'myapp/blog_list.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()

            # Handle tags
            tag_names = form.cleaned_data.get('tags', '').split(',')
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    blog.tags.add(tag)

            messages.success(request, 'Blog post created successfully!')
            return redirect('blog_list')
    else:
        form = BlogForm()
    
    context = {
        'form': form,
        'title': 'Create Blog Post'
    }
    return render(request, 'myapp/create_blog.html', context)

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    context = {
        'blog': blog,
        'title': blog.title,
    }
    return render(request, 'myapp/blog_detail.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            print(f'Contact Form Submission:\\nName: {name}\\nEmail: {email}\\nSubject: {subject}\\nMessage: {message}')
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
        
    context = {
        'form': form,
        'title': 'Contact Us'
    }
    return render(request, 'myapp/contact.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def manage_users(request):
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', '-date_joined')
    
    # Start with all users
    users = User.objects.all()
    
    # Apply search filter
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter == 'admin':
        users = users.filter(is_staff=True)
    elif status_filter == 'user':
        users = users.filter(is_staff=False)
    elif status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # Apply sorting
    if sort_by == 'username':
        users = users.order_by('username')
    elif sort_by == '-username':
        users = users.order_by('-username')
    elif sort_by == 'email':
        users = users.order_by('email')
    elif sort_by == '-email':
        users = users.order_by('-email')
    elif sort_by == 'date_joined':
        users = users.order_by('date_joined')
    else:  # default: -date_joined
        users = users.order_by('-date_joined')
    
    # Get user statistics
    total_users = User.objects.count()
    admin_users = User.objects.filter(is_staff=True).count()
    active_users = User.objects.filter(is_active=True).count()
    recent_users = User.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(days=30)).count()
    
    # Get recipes count for each user
    for user in users:
        user.recipes_count = Recipe.objects.filter(user=user).count()
        user.favorites_count = user.favorite_set.count()
    
    # Pagination
    paginator = Paginator(users, 20)  # Show 20 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'total_users': total_users,
        'admin_users': admin_users,
        'active_users': active_users,
        'recent_users': recent_users,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'title': 'Manage Users'
    }
    return render(request, 'myapp/manage_users.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_user_recipes(request, user_id):
    user = get_object_or_404(User, id=user_id)
    recipes = Recipe.objects.filter(user=user).order_by('-created_at')
    
    # Get user statistics
    total_recipes = recipes.count()
    public_recipes = recipes.filter(is_public=True).count()
    private_recipes = recipes.filter(is_public=False).count()
    total_favorites = user.favorite_set.count()
    
    # Pagination
    paginator = Paginator(recipes, 12)  # Show 12 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'target_user': user,
        'recipes': page_obj,
        'total_recipes': total_recipes,
        'public_recipes': public_recipes,
        'private_recipes': private_recipes,
        'total_favorites': total_favorites,
        'title': f'{user.username}\'s Recipes'
    }
    return render(request, 'myapp/admin_user_recipes.html', context) 