# Recipe Share - Django Recipe Management System

A comprehensive Django web application for sharing, managing, and discovering recipes from around the world. This platform allows users to create, share, and explore recipes with a rich set of features including user management, recipe categorization, blogging, and admin tools.

## 🌟 Features Overview

### 🍳 Recipe Management
- **Create & Share Recipes**: Users can create detailed recipes with ingredients, steps, cooking times, and images
- **Recipe Categorization**: Organize recipes by cuisine type, meal type, difficulty level, and custom tags
- **Recipe Visibility**: Control whether recipes are public or private
- **Recipe Favorites**: Save and organize favorite recipes
- **Recipe Comments**: Engage with other users through comments on recipes
- **Recipe Search & Filter**: Browse recipes by various criteria including cuisine, meal type, and tags

### 👥 User Management
- **User Registration & Authentication**: Secure user registration and login system
- **User Profiles**: Customizable user profiles with avatar uploads
- **User Roles**: Different access levels for regular users, staff members, and administrators
- **Admin Dashboard**: Comprehensive admin tools for user and content management

### 📝 Blogging System
- **Blog Posts**: Create and share cooking-related blog posts
- **Blog Comments**: Interactive commenting system for blog posts
- **Blog Tags**: Categorize blog posts with tags
- **Blog Images**: Support for blog post images

### 🏷️ Content Management
- **Ingredient Management**: Admin tools to manage recipe ingredients
- **Tag Management**: Create and manage recipe and blog tags
- **Cuisine Management**: Organize recipes by world cuisines with country flags
- **Meal Type Management**: Categorize recipes by meal type (breakfast, lunch, dinner, etc.)

### 🎨 User Interface
- **Responsive Design**: Modern, mobile-friendly interface
- **Country Flags**: Visual representation of cuisines using country flags
- **Image Upload**: Support for recipe and profile images
- **Bootstrap 5**: Modern UI framework for consistent styling

## 🏗️ System Architecture

### Models Overview

#### Core Models
- **User**: Extended Django User model with profile functionality
- **Profile**: User profile with avatar support
- **Recipe**: Main recipe entity with comprehensive metadata
- **Blog**: Blog post system for cooking content

#### Recipe-Related Models
- **RecipeIngredient**: Many-to-many relationship between recipes and ingredients
- **Step**: Individual cooking steps for recipes
- **Ingredient**: Reusable ingredients database
- **Unit**: Measurement units for ingredients
- **Tag**: Categorization tags for recipes and blogs
- **RecipeTag**: Many-to-many relationship between recipes and tags

#### Categorization Models
- **Cuisine**: World cuisines with country code support
- **MealType**: Meal categorization (breakfast, lunch, dinner, etc.)
- **Difficulty**: Recipe difficulty levels (Easy, Medium, Hard)

#### Interaction Models
- **Favorite**: User recipe favorites system
- **Comment**: Recipe comments system
- **BlogComment**: Blog post comments system

### Database Design
The system uses SQLite for development with proper indexing on frequently queried fields:
- User-recipe relationships
- Comment timestamps
- Favorite creation dates

## 🚀 Use Cases

### 👤 Guest User Use Cases
1. **Browse Public Recipes**: View all publicly shared recipes
2. **View Recipe Details**: See complete recipe information including ingredients, steps, and comments
3. **Search by Cuisine**: Filter recipes by world cuisines
4. **View Blog Posts**: Read cooking-related blog content
5. **Contact Support**: Send messages to the platform administrators
6. **Register Account**: Create a new user account
7. **Login**: Access existing account

### 👤 Registered User Use Cases
1. **All Guest User Features**: Access to all public content
2. **Create Recipes**: Build detailed recipes with ingredients, steps, and images
3. **Edit Own Recipes**: Modify recipes they've created
4. **Delete Own Recipes**: Remove recipes from the platform
5. **Add to Favorites**: Save interesting recipes to personal favorites
6. **View Favorites**: Access saved favorite recipes
7. **Add Comments**: Engage with recipes through comments
8. **Toggle Recipe Visibility**: Make recipes public or private
9. **Update Profile**: Modify personal profile information
10. **Logout**: Securely log out of the system

### 👨‍💼 Staff Member Use Cases
1. **All Registered User Features**: Full access to user features
2. **Manage Tags**: Create, edit, and delete recipe/blog tags
3. **Manage Ingredients**: Add, modify, and remove ingredients from the database
4. **Manage Cuisines**: Update cuisine information and country codes
5. **Manage Meal Types**: Organize meal type categories

### 👨‍💻 Admin User Use Cases
1. **All Staff Member Features**: Complete content management access
2. **Manage Users**: View, edit, and delete user accounts
3. **View User Recipes**: Access all recipes created by specific users
4. **Create Blog Posts**: Publish cooking-related blog content
5. **Edit Blog Posts**: Modify existing blog content
6. **Delete Blog Posts**: Remove blog posts from the platform
7. **System Administration**: Full platform management capabilities

## 🛠️ Technical Implementation

### Dependencies
```
Django==4.2.1
Pillow==9.4.0
Faker==18.4.0
django-bootstrap5
pycountry
country_converter==1.1.1
gunicorn>=21.2.0
requests
plantuml>=0.3.0
```

### Key Features Implementation

#### Country Flag Integration
- Uses `pycountry` and `country_converter` libraries
- Automatic country code detection for cuisines
- Visual flag representation using Unicode flag emojis

#### Image Management
- Pillow integration for image processing
- Automatic image upload to media directory
- Support for multiple image formats (JPEG, PNG, WebP)

#### Form Management
- Complex form handling with Django formsets
- Dynamic ingredient and step addition
- Form validation and error handling

#### Search and Filtering
- Django ORM-based filtering
- Pagination for large result sets
- Efficient database queries with proper indexing

### Management Commands

#### Data Seeding
- `python manage.py seed_recipes`: Populates database with sample recipes
- `python manage.py seed_blogs`: Creates sample blog posts
- Includes realistic recipe data with images from Unsplash

#### Documentation Generation
- `python manage.py generate_uml_diagram`: Creates UML diagrams for system documentation
- `python manage.py generate_app_use_case`: Generates use case documentation

## 📁 Project Structure

```
djangoClass_duplicate/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── myproject/               # Django project settings
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── myapp/                   # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── urls.py              # URL routing
│   ├── forms.py             # Form definitions
│   ├── templates/           # HTML templates
│   ├── migrations/          # Database migrations
│   └── management/          # Custom management commands
│       └── commands/
│           ├── seed_recipes.py
│           ├── seed_blogs.py
│           ├── generate_uml_diagram.py
│           └── generate_app_use_case.py
└── media/                   # User-uploaded files
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd djangoClass_duplicate
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed database with sample data (optional)**
   ```bash
   python manage.py seed_recipes
   python manage.py seed_blogs
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key (set in production)
- `DEBUG`: Debug mode (set to False in production)
- `ALLOWED_HOSTS`: Allowed host domains

### Media Files
- Configure `MEDIA_ROOT` and `MEDIA_URL` in settings.py
- Ensure media directory is writable
- Set up proper file serving in production

## 🧪 Testing

The application includes comprehensive testing capabilities:
- Unit tests for models and views
- Integration tests for user workflows
- Form validation testing
- Image upload testing

## 📊 Database Management

### Migrations
- All database changes are managed through Django migrations
- Run `python manage.py makemigrations` to create new migrations
- Run `python manage.py migrate` to apply migrations

### Data Seeding
The application includes management commands for populating the database with realistic sample data, including:
- Sample recipes with ingredients and steps
- Blog posts with comments
- User accounts with profiles
- Cuisines with country codes
- Ingredients and measurement units

## 🔒 Security Features

- CSRF protection on all forms
- User authentication and authorization
- Secure file upload handling
- SQL injection prevention through Django ORM
- XSS protection through template escaping

## 🌐 Deployment

### Production Considerations
- Set `DEBUG = False`
- Configure proper `SECRET_KEY`
- Set up production database (PostgreSQL recommended)
- Configure static file serving
- Set up proper media file handling
- Use HTTPS in production
- Configure proper logging

### Recommended Stack
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Database**: PostgreSQL
- **File Storage**: AWS S3 or similar (for media files)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0**: Initial release with core recipe management features
- **v1.1.0**: Added blogging system and enhanced user management
- **v1.2.0**: Improved UI/UX and added country flag support
- **v1.3.0**: Enhanced admin tools and management commands

---

**Recipe Share** - Bringing the world's cuisines together, one recipe at a time! 🍽️ 