from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    
    def __str__(self):
        return self.name

class MealType(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Diet(models.Model):
    name = models.CharField(max_length=50, unique=True)

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
    
    def __str__(self):
        return self.title

class RecipeDiet(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    diet = models.ForeignKey(Diet, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('recipe', 'diet')

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
    
    
