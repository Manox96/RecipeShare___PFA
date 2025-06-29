from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Recipe, Difficulty, Cuisine, MealType, Ingredient, Unit, RecipeIngredient, Step

class Command(BaseCommand):
    help = 'Add 3 recipes for the user with email Emsi_student@emsi.com'

    def handle(self, *args, **kwargs):
        emsi_user, created = User.objects.get_or_create(
            username='Emsi_student',
            email='Emsi_student@emsi.com'
        )
        if created:
            emsi_user.set_password('Emsi_student@emsi.com')
            emsi_user.save()
            self.stdout.write(self.style.SUCCESS('Created user emsi_student'))
        else:
            self.stdout.write(self.style.SUCCESS('User emsi_student already exists'))

        diff = Difficulty.objects.first()
        cuisine = Cuisine.objects.first()
        meal_type = MealType.objects.first()
        ing1 = Ingredient.objects.first()
        ing2 = Ingredient.objects.last()
        unit = Unit.objects.first()

        custom_recipes = [
            {
                'title': 'Emsi Student Salad',
                'description': 'A fresh and simple salad for students.',
                'prep_time': 10,
                'cook_time': 0,
                'servings': 1,
                'ingredients': [
                    {'ingredient': ing1, 'quantity': 100, 'unit': unit},
                ],
                'steps': [
                    'Chop all ingredients.',
                    'Mix in a bowl.',
                    'Serve fresh.'
                ]
            },
            {
                'title': 'Emsi Quick Pasta',
                'description': 'A quick pasta dish for busy students.',
                'prep_time': 5,
                'cook_time': 10,
                'servings': 2,
                'ingredients': [
                    {'ingredient': ing2, 'quantity': 200, 'unit': unit},
                ],
                'steps': [
                    'Boil pasta.',
                    'Add sauce.',
                    'Serve hot.'
                ]
            },
            {
                'title': 'Emsi Power Omelette',
                'description': 'A protein-packed omelette.',
                'prep_time': 3,
                'cook_time': 7,
                'servings': 1,
                'ingredients': [
                    {'ingredient': ing1, 'quantity': 2, 'unit': unit},
                ],
                'steps': [
                    'Beat eggs.',
                    'Cook in pan.',
                    'Fold and serve.'
                ]
            },
        ]

        for r in custom_recipes:
            recipe, created = Recipe.objects.get_or_create(
                title=r['title'],
                user=emsi_user,
                defaults={
                    'description': r['description'],
                    'difficulty': diff,
                    'cuisine': cuisine,
                    'meal_type': meal_type,
                    'prep_time': r['prep_time'],
                    'cook_time': r['cook_time'],
                    'servings': r['servings'],
                    'is_public': True
                }
            )
            if created:
                for ing in r['ingredients']:
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ing['ingredient'],
                        quantity=ing['quantity'],
                        unit=ing['unit']
                    )
                for idx, step in enumerate(r['steps'], 1):
                    Step.objects.create(
                        recipe=recipe,
                        step_number=idx,
                        instruction=step
                    )
                self.stdout.write(self.style.SUCCESS(f'Created recipe: {recipe.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Recipe already exists: {recipe.title}')) 