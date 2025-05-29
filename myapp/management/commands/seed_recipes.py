from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Photo, Recipe, Difficulty, Cuisine, MealType, Ingredient, Unit, RecipeIngredient, Step
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample recipes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding recipes...')

        # Create sample difficulties
        difficulties = [
            Difficulty.objects.get_or_create(name='Easy')[0],
            Difficulty.objects.get_or_create(name='Medium')[0],
            Difficulty.objects.get_or_create(name='Hard')[0],
        ]

        # Create sample cuisines
        cuisines = [
            Cuisine.objects.get_or_create(name='Italian')[0],
            Cuisine.objects.get_or_create(name='Mexican')[0],
            Cuisine.objects.get_or_create(name='Japanese')[0],
            Cuisine.objects.get_or_create(name='Indian')[0],
            Cuisine.objects.get_or_create(name='American')[0],
        ]

        # Create sample meal types
        meal_types = [
            MealType.objects.get_or_create(name='Breakfast')[0],
            MealType.objects.get_or_create(name='Lunch')[0],
            MealType.objects.get_or_create(name='Dinner')[0],
            MealType.objects.get_or_create(name='Dessert')[0],
            MealType.objects.get_or_create(name='Snack')[0],
        ]

        # Create sample ingredients
        ingredients = [
            Ingredient.objects.get_or_create(name='Flour')[0],
            Ingredient.objects.get_or_create(name='Sugar')[0],
            Ingredient.objects.get_or_create(name='Salt')[0],
            Ingredient.objects.get_or_create(name='Eggs')[0],
            Ingredient.objects.get_or_create(name='Milk')[0],
            Ingredient.objects.get_or_create(name='Butter')[0],
            Ingredient.objects.get_or_create(name='Chicken')[0],
            Ingredient.objects.get_or_create(name='Rice')[0],
            Ingredient.objects.get_or_create(name='Tomatoes')[0],
            Ingredient.objects.get_or_create(name='Onions')[0],
        ]

        # Create sample units
        units = [
            Unit.objects.get_or_create(name='grams')[0],
            Unit.objects.get_or_create(name='cups')[0],
            Unit.objects.get_or_create(name='tablespoons')[0],
            Unit.objects.get_or_create(name='teaspoons')[0],
            Unit.objects.get_or_create(name='pieces')[0],
        ]

        # Sample recipes data
        recipes_data = [
            {
                'title': 'Classic Margherita Pizza',
                'description': 'A traditional Italian pizza with fresh tomatoes, mozzarella, and basil.',
                'difficulty': difficulties[0],
                'cuisine': cuisines[0],
                'meal_type': meal_types[2],
                'prep_time': 30,
                'cook_time': 15,
                'servings': 4,
                'ingredients': [
                    {'ingredient': ingredients[0], 'quantity': 500, 'unit': units[0]},  # Flour
                    {'ingredient': ingredients[1], 'quantity': 1, 'unit': units[2]},     # Sugar
                    {'ingredient': ingredients[2], 'quantity': 1, 'unit': units[2]},     # Salt
                    {'ingredient': ingredients[3], 'quantity': 1, 'unit': units[4]},     # Eggs
                ],
                'steps': [
                    'Mix flour, sugar, and salt in a large bowl',
                    'Add eggs and mix until a dough forms',
                    'Knead the dough for 10 minutes',
                    'Let the dough rest for 1 hour',
                    'Roll out the dough and add toppings',
                    'Bake at 450°F for 15 minutes'
                ]
            },
            {
                'title': 'Chicken Curry',
                'description': 'A flavorful Indian curry with tender chicken pieces in a rich sauce.',
                'difficulty': difficulties[1],
                'cuisine': cuisines[3],
                'meal_type': meal_types[2],
                'prep_time': 20,
                'cook_time': 40,
                'servings': 6,
                'ingredients': [
                    {'ingredient': ingredients[6], 'quantity': 1000, 'unit': units[0]},  # Chicken
                    {'ingredient': ingredients[7], 'quantity': 2, 'unit': units[1]},     # Rice
                    {'ingredient': ingredients[8], 'quantity': 4, 'unit': units[4]},     # Tomatoes
                    {'ingredient': ingredients[9], 'quantity': 2, 'unit': units[4]},     # Onions
                ],
                'steps': [
                    'Cut chicken into pieces',
                    'Chop onions and tomatoes',
                    'Cook onions until golden',
                    'Add chicken and cook until browned',
                    'Add tomatoes and spices',
                    'Simmer for 30 minutes',
                    'Serve with rice'
                ]
            },
            {
                'title': 'Chocolate Chip Cookies',
                'description': 'Classic American cookies with chocolate chips.',
                'difficulty': difficulties[0],
                'cuisine': cuisines[4],
                'meal_type': meal_types[3],
                'prep_time': 15,
                'cook_time': 12,
                'servings': 24,
                'ingredients': [
                    {'ingredient': ingredients[0], 'quantity': 250, 'unit': units[0]},  # Flour
                    {'ingredient': ingredients[1], 'quantity': 200, 'unit': units[0]},  # Sugar
                    {'ingredient': ingredients[5], 'quantity': 200, 'unit': units[0]},  # Butter
                    {'ingredient': ingredients[3], 'quantity': 2, 'unit': units[4]},    # Eggs
                ],
                'steps': [
                    'Cream butter and sugar',
                    'Add eggs and mix well',
                    'Add flour and mix until combined',
                    'Fold in chocolate chips',
                    'Drop spoonfuls onto baking sheet',
                    'Bake at 350°F for 12 minutes'
                ]
            }
        ]

        # Create a test user if it doesn't exist
        test_user, created = User.objects.get_or_create(
            username='testuser',
            email='test@example.com'
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()

        # Create recipes
        for recipe_data in recipes_data:
            # Create the recipe
            recipe = Recipe.objects.create(
                title=recipe_data['title'],
                description=recipe_data['description'],
                difficulty=recipe_data['difficulty'],
                cuisine=recipe_data['cuisine'],
                meal_type=recipe_data['meal_type'],
                prep_time=recipe_data['prep_time'],
                cook_time=recipe_data['cook_time'],
                servings=recipe_data['servings'],
                user=test_user,
                created_at=timezone.now()
            )

            # Create ingredients
            for ingredient_data in recipe_data['ingredients']:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient_data['ingredient'],
                    quantity=ingredient_data['quantity'],
                    unit=ingredient_data['unit']
                )

            # Create steps
            for index, step_text in enumerate(recipe_data['steps'], 1):
                Step.objects.create(
                    recipe=recipe,
                    step_number=index,
                    instruction=step_text
                )

            self.stdout.write(self.style.SUCCESS(f'Created recipe: {recipe.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded recipes')) 