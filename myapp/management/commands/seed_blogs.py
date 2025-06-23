from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Blog, Tag
import urllib.request
from django.core.files import File
import ssl

class Command(BaseCommand):
    help = 'Deletes all existing blogs and seeds the database with new sample blog posts with images.'

    def handle(self, *args, **kwargs):
        # Temporarily bypass SSL verification for downloading images.
        # This is for local development seeding only.
        ssl._create_default_https_context = ssl._create_unverified_context
        
        self.stdout.write('Deleting old blog posts...')
        Blog.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Old blog posts deleted.'))

        self.stdout.write('Seeding new blogs...')

        # Find or create an admin user
        admin_user, created = User.objects.get_or_create(
            username='admin', 
            defaults={'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create sample tags
        tags = [
            Tag.objects.get_or_create(name='Burgers')[0],
            Tag.objects.get_or_create(name='Inspiration')[0],
            Tag.objects.get_or_create(name='Mindful Eating')[0],
            Tag.objects.get_or_create(name='Creativity')[0],
            Tag.objects.get_or_create(name='Flavor')[0],
        ]
        
        blog_posts = [
            {
                'title': 'Homemade Burger Night Done Right',
                'content': "Great recipes begin with inspiration, and every dish tells a story waiting to be shared. Whether you're exploring new flavors, mastering techniques, or learning about unique ingredients, there's always something exciting to discover in the kitchen. Our blog is designed to fuel your culinary creativity, offering fresh ideas, practical tips, and in-depth insights to make your time in the kitchen more enjoyable and fulfilling. From finding the perfect balance of spices to discovering the health benefits of certain ingredients, we aim to help you cook confidently and joyfully. No matter your skill level, whether you're a beginner trying your hand at simple meals or an experienced cook seeking new challenges, you'll find something valuable here. Let every recipe be an opportunity to learn, grow, and, most importantly, enjoy the process of creating delicious, memorable food for yourself and others.",
                'tags': [tags[0], tags[1]],
                'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=1998&auto=format&fit=crop'
            },
            {
                'title': 'From Quick Meals to Detailed Guides',
                'content': "From quick meal ideas to detailed guides, our blog covers a variety of topics to meet your needs and interests. Discover healthy options for mindful eating, time-saving hacks for busy days, and step-by-step instructions for mastering dishes. We also feature ingredient spotlights, seasonal recipes, and expert advice to take your cooking skills to the next level. Whether you're whipping up a simple weeknight dinner, experimenting with new flavors, or preparing an elaborate meal for a special occasion, our content is here to inspire, educate, and bring excitement to your culinary adventures. With our guidance, your kitchen will always be a place of creativity and joy",
                'tags': [tags[2], tags[1]],
                'image_url': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?q=80&w=1974&auto=format&fit=crop'
            },
            {
                'title': 'Finding Joy in Every Delicious Bite',
                'content': "Discovering the art of cooking can be a rewarding journey, blending creativity and technique. Whether you're experimenting with new recipes or perfecting your go-to favorites, the kitchen offers endless possibilities. Every ingredient holds potential, and every dish can be a canvas for expression. From selecting fresh produce to adding the right seasoning, each step matters. Exploring various cooking methods and understanding how flavors interact help you create meals that are not just tasty, but memorable. Whether you're whipping up a quick dinner or a lavish feast, cooking is an experience that connects us with culture, tradition, and innovation. A simple meal can bring people together, create lasting memories, and provide comfort. As you explore different recipes, don't be afraid to tweak ingredients, adjust seasonings, or try new techniques. Trust your instincts and enjoy the journey.",
                'tags': [tags[3], tags[4]],
                'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=1981&auto=format&fit=crop'
            },
            {
                'title': 'A Blend of Creativity, Skill, and Exploration',
                'content': "Cooking is a beautiful blend of creativity, skill, and exploration. From selecting fresh ingredients to perfecting flavors, every step contributes to a satisfying meal. The kitchen is a place where you can experiment, make mistakes, and learn. Each dish is a reflection of your tastes, techniques, and passion. Embrace the process of cooking with curiosity—try new recipes, tweak ingredients, and discover the joy of creating something delicious. Whether you're preparing a simple meal or a lavish feast, the act of cooking nourishes both the body and the soul. Enjoy the textures, aromas, and colors that come together to form a dish. Cooking is not just about feeding yourself or others; it's about expressing creativity, sharing moments, and turning ordinary ingredients into extraordinary experiences.",
                'tags': [tags[3], tags[4]],
                'image_url': 'https://images.unsplash.com/photo-1565958011703-44f9829ba187?q=80&w=1965&auto=format&fit=crop'
            },
            {
                'title': 'Where Flavor Meets Creativity',
                'content': "Exploring new recipes can be an exciting adventure that sparks creativity in the kitchen. Whether you're trying a simple dish or a complex one, each step is an opportunity to learn and grow. Embrace the joy of selecting fresh ingredients, experimenting with flavors, and discovering unique techniques. Cooking isn't just about following a recipe — it's about making it your own. Every sprinkle of spice, every new ingredient, and every taste test brings you closer to creating something delicious. The kitchen is where inspiration meets preparation, and where even small successes lead to satisfying meals and memorable moments. The best part of cooking is sharing the experience with loved ones or enjoying the satisfaction of a meal well made. Simple tips, quick hacks, and creative ideas can make a big difference in your cooking journey. From mastering knife skills to learning how to balance flavors, every skill adds to your confidence. Don't hesitate to try new cuisines, mix unexpected ingredients, or tweak recipes to suit your taste. Cooking is more than just a daily task — it's an experience filled with joy, learning, and endless possibilities. Let every recipe remind you of the joy in creating something delicious from scratch",
                'tags': [tags[4], tags[3]],
                'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=1780&auto=format&fit=crop'
            }
        ]

        for post_data in blog_posts:
            blog = Blog.objects.create(
                title=post_data['title'],
                content=post_data['content'],
                author=admin_user
            )

            # Attach image
            if post_data.get('image_url'):
                try:
                    result = urllib.request.urlretrieve(post_data['image_url'])
                    blog.image.save(
                        f"blog_{blog.id}.jpg", 
                        File(open(result[0], 'rb'))
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Could not process image for {blog.title}: {e}'))

            blog.tags.set(post_data['tags'])
            self.stdout.write(self.style.SUCCESS(f'Created blog post: {blog.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded blogs')) 