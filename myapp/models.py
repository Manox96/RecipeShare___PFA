from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import pycountry
import country_converter as coco
from django.conf import settings

# Create your models here.
class Photo(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    Nom = models.CharField(max_length=200)
    Descreption = models.TextField(blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_photos', blank=True)
    
    def __str__(self):
        return self.Nom

# Recipe-related models
class Difficulty(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Cuisine(models.Model):
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=5, blank=True, null=True, help_text='ISO country code for flag display')

    def save(self, *args, **kwargs):
        if not self.country_code or self.country_code == 'not found':
            # Handle special cases first
            if self.name == 'American':
                self.country_code = 'US'
            elif self.name == 'Moroccan':
                self.country_code = 'MA'
            else:
                try:
                    # Use country_converter to find the ISO2 code
                    self.country_code = coco.convert(names=self.name, to='ISO2')
                except Exception:
                    # If that fails, try with pycountry as a fallback
                    try:
                        country = pycountry.countries.get(name=self.name)
                        if country:
                            self.country_code = country.alpha_2
                    except (AttributeError, KeyError):
                        self.country_code = None  # Or a default value
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class MealType(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True)
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE)
    prep_time = models.IntegerField(help_text='Preparation time in minutes')
    cook_time = models.IntegerField(help_text='Cooking time in minutes')
    servings = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    is_public = models.BooleanField(default=True, help_text='If checked, this recipe will be visible on the main page')
    tags = models.ManyToManyField('Tag', through='RecipeTag', blank=True)
    
    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient}"

class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField()
    instruction = models.TextField()
    
    class Meta:
        ordering = ['step_number']
    
    def __str__(self):
        return f"Step {self.step_number} of {self.recipe.title}"

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('recipe', 'tag')

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'recipe')
        indexes = [
            models.Index(fields=['user', 'recipe']),
            models.Index(fields=['created_at']),
        ]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['recipe']),
            models.Index(fields=['created_at']),
        ]

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BlogComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['blog']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    
