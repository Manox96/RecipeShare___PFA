from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Photo, Recipe, Difficulty, Cuisine, MealType, Ingredient, Unit, RecipeIngredient, Step
from django.utils import timezone
import random
import requests
import os
from django.core.files.base import ContentFile
import mimetypes
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Seeds the database with sample recipes'

    def download_image(self, image_url, recipe_title):
        """Download image from URL and return ContentFile"""
        try:
            # Add proper Unsplash parameters if not present
            if 'unsplash.com' in image_url and '?' not in image_url:
                image_url += '?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60'
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(image_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Determine file extension from content type
            content_type = response.headers.get('content-type', '')
            if 'image/jpeg' in content_type:
                extension = '.jpg'
            elif 'image/png' in content_type:
                extension = '.png'
            elif 'image/webp' in content_type:
                extension = '.webp'
            else:
                extension = '.jpg'  # default
            
            # Create a safe filename
            safe_title = "".join(c for c in recipe_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            filename = f"{safe_title}{extension}"
            
            return ContentFile(response.content), filename
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.WARNING(f"Could not download image for {recipe_title}: {e}"))
            return None, None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Unexpected error downloading image for {recipe_title}: {e}"))
            return None, None

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old recipes...')
        Recipe.objects.all().delete()
        Difficulty.objects.all().delete()
        Cuisine.objects.all().delete()
        MealType.objects.all().delete()
        Ingredient.objects.all().delete()
        Unit.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Old recipe data deleted.'))
        
        self.stdout.write('Seeding recipes...')

        # Create sample difficulties
        difficulties = [
            Difficulty.objects.get_or_create(name='Easy')[0],
            Difficulty.objects.get_or_create(name='Medium')[0],
            Difficulty.objects.get_or_create(name='Hard')[0],
        ]

        # Create sample cuisines
        cuisines = [
            Cuisine.objects.get_or_create(name='Italian', defaults={'country_code': 'IT'})[0],
            Cuisine.objects.get_or_create(name='Mexican', defaults={'country_code': 'MX'})[0],
            Cuisine.objects.get_or_create(name='Japanese', defaults={'country_code': 'JP'})[0],
            Cuisine.objects.get_or_create(name='Indian', defaults={'country_code': 'IN'})[0],
            Cuisine.objects.get_or_create(name='American', defaults={'country_code': 'US'})[0],
            Cuisine.objects.get_or_create(name='Spanish', defaults={'country_code': 'ES'})[0],
            Cuisine.objects.get_or_create(name='French', defaults={'country_code': 'FR'})[0],
            Cuisine.objects.get_or_create(name='Chinese', defaults={'country_code': 'CN'})[0],
            Cuisine.objects.get_or_create(name='Thai', defaults={'country_code': 'TH'})[0],
            Cuisine.objects.get_or_create(name='Greek', defaults={'country_code': 'GR'})[0],
            Cuisine.objects.get_or_create(name='Korean', defaults={'country_code': 'KR'})[0],
            Cuisine.objects.get_or_create(name='Vietnamese', defaults={'country_code': 'VN'})[0],
            Cuisine.objects.get_or_create(name='Lebanese', defaults={'country_code': 'LB'})[0],
            Cuisine.objects.get_or_create(name='Moroccan', defaults={'country_code': 'MA'})[0],
            Cuisine.objects.get_or_create(name='German', defaults={'country_code': 'DE'})[0],
        ]

        # Create sample meal types
        meal_types = [
            MealType.objects.get_or_create(name='Breakfast')[0],
            MealType.objects.get_or_create(name='Lunch')[0],
            MealType.objects.get_or_create(name='Dinner')[0],
            MealType.objects.get_or_create(name='Dessert')[0],
            MealType.objects.get_or_create(name='Snack')[0],
            MealType.objects.get_or_create(name='Appetizer')[0],
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
            Ingredient.objects.get_or_create(name='Garlic')[0],
            Ingredient.objects.get_or_create(name='Olive Oil')[0],
            Ingredient.objects.get_or_create(name='Pasta')[0],
            Ingredient.objects.get_or_create(name='Cheese')[0],
            Ingredient.objects.get_or_create(name='Beef')[0],
            Ingredient.objects.get_or_create(name='Pork')[0],
            Ingredient.objects.get_or_create(name='Soy Sauce')[0],
            Ingredient.objects.get_or_create(name='Ginger')[0],
            Ingredient.objects.get_or_create(name='Lime')[0],
            Ingredient.objects.get_or_create(name='Fish Sauce')[0],
            Ingredient.objects.get_or_create(name='Coconut Milk')[0],
            Ingredient.objects.get_or_create(name='Cilantro')[0],
            Ingredient.objects.get_or_create(name='Jalapeño')[0],
            Ingredient.objects.get_or_create(name='Avocado')[0],
            Ingredient.objects.get_or_create(name='Feta Cheese')[0],
            Ingredient.objects.get_or_create(name='Cucumber')[0],
            Ingredient.objects.get_or_create(name='Yogurt')[0],
            Ingredient.objects.get_or_create(name='Gochujang')[0],
            Ingredient.objects.get_or_create(name='Kimchi')[0],
            Ingredient.objects.get_or_create(name='Rice Noodles')[0],
            Ingredient.objects.get_or_create(name='Mint')[0],
            Ingredient.objects.get_or_create(name='Parsley')[0],
            Ingredient.objects.get_or_create(name='Chickpeas')[0],
            Ingredient.objects.get_or_create(name='Tahini')[0],
            Ingredient.objects.get_or_create(name='Cumin')[0],
            Ingredient.objects.get_or_create(name='Cinnamon')[0],
            Ingredient.objects.get_or_create(name='Potatoes')[0],
            Ingredient.objects.get_or_create(name='Sausage')[0],
            Ingredient.objects.get_or_create(name='Sauerkraut')[0],
            Ingredient.objects.get_or_create(name='Bell Pepper')[0],
            Ingredient.objects.get_or_create(name='Shrimp')[0],
            Ingredient.objects.get_or_create(name='Scallions')[0],
            Ingredient.objects.get_or_create(name='Sesame Oil')[0],
        ]

        # Create sample units
        units = [
            Unit.objects.get_or_create(name='grams')[0],
            Unit.objects.get_or_create(name='cups')[0],
            Unit.objects.get_or_create(name='tablespoons')[0],
            Unit.objects.get_or_create(name='teaspoons')[0],
            Unit.objects.get_or_create(name='pieces')[0],
            Unit.objects.get_or_create(name='cloves')[0],
            Unit.objects.get_or_create(name='ml')[0],
            Unit.objects.get_or_create(name='inch')[0],
            Unit.objects.get_or_create(name='bunch')[0],
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
                'image_url': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
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
                'image_url': 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
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
                'image_url': 'https://images.unsplash.com/photo-1590947132387-155cc02f3212?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
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
            },
            {
                'title': 'Spaghetti Carbonara',
                'description': 'A classic Italian pasta dish with eggs, cheese, pancetta, and pepper.',
                'difficulty': difficulties[1],
                'cuisine': cuisines[0],
                'meal_type': meal_types[2],
                'prep_time': 15,
                'cook_time': 20,
                'servings': 4,
                'image_url': 'https://images.unsplash.com/photo-1559314809-0d155014e29e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[12], 'quantity': 400, 'unit': units[0]}, # Pasta
                    {'ingredient': ingredients[3], 'quantity': 4, 'unit': units[4]}, # Eggs
                    {'ingredient': ingredients[13], 'quantity': 150, 'unit': units[0]}, # Cheese
                    {'ingredient': ingredients[10], 'quantity': 2, 'unit': units[5]}, # Garlic
                ],
                'steps': [
                    'Cook pasta according to package instructions.',
                    'While pasta is cooking, cook pancetta in a large skillet.',
                    'In a bowl, whisk together eggs, cheese, and black pepper.',
                    'Drain pasta and add it to the skillet with the pancetta.',
                    'Remove from heat and quickly stir in the egg mixture.',
                    'Serve immediately with extra cheese.'
                ]
            },
            {
                'title': 'Beef Tacos',
                'description': 'Classic Mexican tacos with seasoned ground beef and fresh toppings.',
                'difficulty': difficulties[0],
                'cuisine': cuisines[1],
                'meal_type': meal_types[2],
                'prep_time': 20,
                'cook_time': 15,
                'servings': 4,
                'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[14], 'quantity': 500, 'unit': units[0]}, # Beef
                    {'ingredient': ingredients[9], 'quantity': 1, 'unit': units[4]}, # Onions
                    {'ingredient': ingredients[8], 'quantity': 2, 'unit': units[4]}, # Tomatoes
                ],
                'steps': [
                    'Cook ground beef with chopped onions until browned.',
                    'Stir in taco seasoning and water, then simmer.',
                    'Warm taco shells in the oven.',
                    'Assemble tacos with beef, lettuce, tomato, and cheese.'
                ]
            },
            {
                'title': 'French Onion Soup',
                'description': 'A rich and savory soup made with caramelized onions and beef broth, topped with melted cheese.',
                'difficulty': difficulties[2],
                'cuisine': cuisines[6],
                'meal_type': meal_types[5],
                'prep_time': 20,
                'cook_time': 60,
                'servings': 4,
                'image_url': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[9], 'quantity': 4, 'unit': units[4]}, # Onions
                    {'ingredient': ingredients[5], 'quantity': 50, 'unit': units[0]}, # Butter
                    {'ingredient': ingredients[11], 'quantity': 50, 'unit': units[6]}, # Olive Oil
                ],
                'steps': [
                    'Slice onions thinly and caramelize them in butter and olive oil.',
                    'Add beef broth and simmer.',
                    'Ladle soup into oven-safe bowls.',
                    'Top with a slice of bread and a generous amount of Gruyère cheese.',
                    'Broil until cheese is bubbly and golden.'
                ]
            },
            {
                'title': 'Spanish Paella',
                'description': 'A flavorful Spanish rice dish with saffron, seafood, and vegetables.',
                'difficulty': difficulties[2],
                'cuisine': cuisines[5],
                'meal_type': meal_types[2],
                'prep_time': 25,
                'cook_time': 35,
                'servings': 6,
                'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[7], 'quantity': 400, 'unit': units[0]}, # Rice
                    {'ingredient': ingredients[6], 'quantity': 200, 'unit': units[0]}, # Chicken
                    {'ingredient': ingredients[8], 'quantity': 2, 'unit': units[4]}, # Tomatoes
                ],
                'steps': [
                    'Sauté chicken and vegetables in a paella pan.',
                    'Add rice and saffron-infused broth.',
                    'Arrange seafood on top and cook until the rice is tender and the liquid is absorbed.',
                    'Let it rest for a few minutes before serving.'
                ]
            },
            {
                'title': 'Kung Pao Chicken',
                'description': 'A spicy, stir-fried Chinese dish made with chicken, peanuts, vegetables, and chili peppers.',
                'difficulty': difficulties[1],
                'cuisine': cuisines[7],
                'meal_type': meal_types[2],
                'prep_time': 20,
                'cook_time': 15,
                'servings': 4,
                'image_url': 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[6], 'quantity': 500, 'unit': units[0]}, # Chicken
                    {'ingredient': ingredients[10], 'quantity': 2, 'unit': units[5]}, # Garlic
                    {'ingredient': ingredients[9], 'quantity': 1, 'unit': units[4]}, # Onions
                ],
                'steps': [
                    'Marinate chicken in soy sauce and cornstarch.',
                    'Stir-fry chicken until golden brown.',
                    'Add vegetables, peanuts, and chili peppers.',
                    'Toss with Kung Pao sauce and serve.'
                ]
            },
            {
                'title': 'Pad Thai',
                'description': 'A popular Thai stir-fried noodle dish with shrimp, tofu, peanuts, and a tangy sauce.',
                'difficulty': difficulties[1],
                'cuisine': cuisines[8],
                'meal_type': meal_types[2],
                'prep_time': 25,
                'cook_time': 15,
                'servings': 4,
                'image_url': 'https://images.unsplash.com/photo-1559314809-0d155014e29e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[32], 'quantity': 200, 'unit': units[0]}, # Rice Noodles
                    {'ingredient': ingredients[3], 'quantity': 2, 'unit': units[4]}, # Eggs
                    {'ingredient': ingredients[6], 'quantity': 200, 'unit': units[0]}, # Chicken
                ],
                'steps': [
                    'Soak rice noodles in warm water.',
                    'Stir-fry shrimp and tofu.',
                    'Add noodles, bean sprouts, and Pad Thai sauce.',
                    'Scramble an egg into the noodles.',
                    'Serve with crushed peanuts, lime, and cilantro.'
                ]
            },
            {
                'title': 'Greek Moussaka',
                'description': 'A layered oven-baked dish with eggplant, minced meat, and a creamy béchamel sauce.',
                'difficulty': difficulties[2],
                'cuisine': cuisines[9],
                'meal_type': meal_types[2],
                'prep_time': 45,
                'cook_time': 60,
                'servings': 8,
                'image_url': 'https://images.unsplash.com/photo-1590947132387-155cc02f3212?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[14], 'quantity': 500, 'unit': units[0]}, # Beef
                    {'ingredient': ingredients[8], 'quantity': 400, 'unit': units[0]}, # Tomatoes
                    {'ingredient': ingredients[38], 'quantity': 1, 'unit': units[3]}, # Cinnamon
                ],
                'steps': [
                    'Slice and salt eggplant, then fry until golden.',
                    'Prepare a rich meat sauce with tomatoes and spices.',
                    'Make a creamy béchamel sauce.',
                    'Layer the eggplant, meat sauce, and béchamel in a baking dish.',
                    'Bake until golden and bubbly.'
                ]
            },
            {
                'title': 'Korean Bibimbap',
                'description': 'A vibrant Korean rice bowl topped with assorted vegetables, beef, a fried egg, and gochujang sauce.',
                'difficulty': difficulties[1],
                'cuisine': cuisines[10],
                'meal_type': meal_types[2],
                'prep_time': 30,
                'cook_time': 15,
                'servings': 2,
                'image_url': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[7], 'quantity': 2, 'unit': units[1]}, # Rice
                    {'ingredient': ingredients[14], 'quantity': 200, 'unit': units[0]}, # Beef
                    {'ingredient': ingredients[28], 'quantity': 30, 'unit': units[6]}, # Gochujang
                ],
                'steps': [
                    'Cook rice and prepare assorted vegetables (sautéed, blanched).',
                    'Marinate and cook beef.',
                    'Assemble by placing vegetables and beef over rice in a bowl.',
                    'Top with a fried egg and a dollop of gochujang.',
                    'Mix everything together before eating.'
                ]
            },
            {
                'title': 'Vietnamese Pho',
                'description': 'A fragrant and flavorful Vietnamese noodle soup with a rich broth, rice noodles, herbs, and meat.',
                'difficulty': difficulties[2],
                'cuisine': cuisines[11],
                'meal_type': meal_types[2],
                'prep_time': 20,
                'cook_time': 180,
                'servings': 6,
                'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[32], 'quantity': 500, 'unit': units[0]}, # Rice Noodles
                    {'ingredient': ingredients[14], 'quantity': 500, 'unit': units[0]}, # Beef
                    {'ingredient': ingredients[17], 'quantity': 2, 'unit': units[7]}, # Ginger
                ],
                'steps': [
                    'Simmer beef bones, charred ginger, and onion for hours to create the broth.',
                    'Strain the broth and season with fish sauce and spices.',
                    'Cook rice noodles.',
                    'Assemble bowls with noodles, thinly sliced raw beef, and herbs.',
                    'Pour hot broth over the top to cook the beef.'
                ]
            },
            {
                'title': 'Lebanese Hummus',
                'description': 'A creamy and smooth dip made from chickpeas, tahini, lemon juice, and garlic.',
                'difficulty': difficulties[0],
                'cuisine': cuisines[12],
                'meal_type': meal_types[5],
                'prep_time': 15,
                'cook_time': 0,
                'servings': 6,
                'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[35], 'quantity': 400, 'unit': units[0]}, # Chickpeas
                    {'ingredient': ingredients[36], 'quantity': 120, 'unit': units[6]}, # Tahini
                    {'ingredient': ingredients[10], 'quantity': 2, 'unit': units[5]}, # Garlic
                ],
                'steps': [
                    'Blend cooked chickpeas, tahini, lemon juice, and garlic until smooth.',
                    'Add a little water or olive oil to reach the desired consistency.',
                    'Season with salt.',
                    'Serve drizzled with olive oil and a sprinkle of paprika or parsley.'
                ]
            },
            {
                'title': 'Moroccan Tagine',
                'description': 'A slow-cooked savory stew from North Africa, traditionally cooked in a conical earthenware pot.',
                'difficulty': difficulties[2],
                'cuisine': cuisines[13],
                'meal_type': meal_types[2],
                'prep_time': 30,
                'cook_time': 120,
                'servings': 6,
                'image_url': 'https://images.unsplash.com/photo-1551218808-94e220e084d2?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[6], 'quantity': 1000, 'unit': units[0]}, # Chicken
                    {'ingredient': ingredients[9], 'quantity': 2, 'unit': units[4]}, # Onions
                    {'ingredient': ingredients[37], 'quantity': 1, 'unit': units[3]}, # Cumin
                ],
                'steps': [
                    'Brown the chicken or lamb in a tagine or Dutch oven.',
                    'Add onions, garlic, and a blend of Moroccan spices like cumin, turmeric, and ginger.',
                    'Add liquid (broth or water) and bring to a simmer.',
                    'Cover and cook on low heat for 1-2 hours until the meat is tender.',
                    'Add vegetables, dried fruit, or olives during the last 30 minutes of cooking.'
                ]
            },
            {
                'title': 'German Schnitzel',
                'description': 'A thin slice of meat, typically pork or veal, breaded and fried.',
                'difficulty': difficulties[1],
                'cuisine': cuisines[14],
                'meal_type': meal_types[2],
                'prep_time': 20,
                'cook_time': 10,
                'servings': 4,
                'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
                'ingredients': [
                    {'ingredient': ingredients[15], 'quantity': 4, 'unit': units[4]}, # Pork
                    {'ingredient': ingredients[0], 'quantity': 1, 'unit': units[1]}, # Flour
                    {'ingredient': ingredients[3], 'quantity': 2, 'unit': units[4]}, # Eggs
                ],
                'steps': [
                    'Pound meat cutlets to an even thickness.',
                    'Set up a breading station with flour, beaten eggs, and breadcrumbs.',
                    'Dredge each cutlet in flour, dip in egg, and coat with breadcrumbs.',
                    'Pan-fry in hot oil or butter until golden brown on both sides.',
                    'Serve with lemon wedges.'
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
            recipe = Recipe(
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

            # Download and save the image
            if recipe_data.get('image_url'):
                content_file, filename = self.download_image(recipe_data['image_url'], recipe_data['title'])
                if content_file and filename:
                    recipe.image.save(filename, content_file, save=False)
                    self.stdout.write(self.style.SUCCESS(f'Downloaded image for: {recipe_data["title"]}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Failed to download image for: {recipe_data["title"]}'))

            recipe.save()

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