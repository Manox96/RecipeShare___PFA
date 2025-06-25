from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Recipe, Blog, Tag, Ingredient, Cuisine, MealType, Difficulty, Unit, Photo, Favorite, Comment, Profile
import os
import tempfile
import subprocess

class Command(BaseCommand):
    help = 'Generates a comprehensive use case diagram based on the actual Recipe Share application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='recipe_share_use_case',
            help='Output filename (without extension)'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['png', 'svg', 'pdf'],
            default='png',
            help='Output format'
        )

    def generate_comprehensive_use_case_diagram(self, output_file, format_type):
        """Generate a comprehensive use case diagram based on the actual app functionality"""
        
        plantuml_code = """@startuml
left to right direction
skinparam packageStyle rectangle
skinparam usecase {
    BackgroundColor LightBlue
    BorderColor DarkBlue
    ArrowColor DarkBlue
}
skinparam actor {
    BackgroundColor LightGreen
    BorderColor DarkGreen
}
skinparam rectangle {
    BackgroundColor LightYellow
    BorderColor DarkOrange
}

' Primary Actors
:Guest User: as GU
:Registered User: as RU
:Admin User: as AU
:Staff Member: as SM

' Secondary Actors
:Email System: as ES
:File System: as FS
:Database: as DB

rectangle "Recipe Share System" {
    package "Authentication & User Management" {
        (Register Account) as UC1
        (Login) as UC2
        (Logout) as UC3
        (View Profile) as UC4
        (Update Profile) as UC5
        (Upload Avatar) as UC6
    }
    
    package "Public Recipe Browsing" {
        (Browse Public Recipes) as UC7
        (View Recipe Details) as UC8
        (Filter by Meal Type) as UC9
        (Filter by Cuisine) as UC10
        (Search Recipes) as UC11
        (View Popular Recipes) as UC12
        (View New Recipes) as UC13
    }
    
    package "Recipe Management" {
        (Create Recipe) as UC14
        (Edit Recipe) as UC15
        (Delete Recipe) as UC16
        (Add Recipe Image) as UC17
        (Set Recipe Visibility) as UC18
        (Add Recipe Ingredients) as UC19
        (Add Recipe Steps) as UC20
        (Add Recipe Tags) as UC21
    }
    
    package "Social Features" {
        (Add to Favorites) as UC22
        (View Favorites) as UC23
        (Remove from Favorites) as UC24
        (Add Comment) as UC25
        (View Comments) as UC26
    }
    
    package "Content Management" {
        (Manage Users) as UC27
        (Edit User Details) as UC28
        (Delete User) as UC29
        (View User Recipes) as UC30
        (Manage Tags) as UC31
        (Create Tag) as UC32
        (Edit Tag) as UC33
        (Delete Tag) as UC34
        (Manage Ingredients) as UC35
        (Create Ingredient) as UC36
        (Edit Ingredient) as UC37
        (Delete Ingredient) as UC38
        (Manage Units) as UC39
    }
    
    package "Blog System" {
        (View Blog Posts) as UC40
        (Create Blog Post) as UC41
        (Edit Blog Post) as UC42
        (Delete Blog Post) as UC43
        (Add Blog Image) as UC44
        (Add Blog Tags) as UC45
    }
    
    package "Photo Management" {
        (Upload Photo) as UC46
        (View Photos) as UC47
        (Delete Photo) as UC48
        (Add Photo to Favorites) as UC49
        (View Favorite Photos) as UC50
    }
    
    package "Communication" {
        (Contact Support) as UC51
        (View Cooking Tips) as UC52
    }
    
    package "System Features" {
        (View Recipe Statistics) as UC53
        (Export Recipe Data) as UC54
        (Backup User Data) as UC55
    }
}

' Guest User associations
GU --> UC1
GU --> UC2
GU --> UC7
GU --> UC8
GU --> UC9
GU --> UC10
GU --> UC11
GU --> UC12
GU --> UC13
GU --> UC40
GU --> UC51
GU --> UC52

' Registered User associations
RU --> UC3
RU --> UC4
RU --> UC5
RU --> UC6
RU --> UC7
RU --> UC8
RU --> UC9
RU --> UC10
RU --> UC11
RU --> UC12
RU --> UC13
RU --> UC14
RU --> UC15
RU --> UC16
RU --> UC17
RU --> UC18
RU --> UC19
RU --> UC20
RU --> UC21
RU --> UC22
RU --> UC23
RU --> UC24
RU --> UC25
RU --> UC26
RU --> UC40
RU --> UC46
RU --> UC47
RU --> UC48
RU --> UC49
RU --> UC50
RU --> UC51
RU --> UC52

' Admin User associations
AU --> UC27
AU --> UC28
AU --> UC29
AU --> UC30
AU --> UC41
AU --> UC42
AU --> UC43
AU --> UC44
AU --> UC45
AU --> UC51
AU --> UC53
AU --> UC54
AU --> UC55

' Staff Member associations
SM --> UC31
SM --> UC32
SM --> UC33
SM --> UC34
SM --> UC35
SM --> UC36
SM --> UC37
SM --> UC38
SM --> UC39

' Secondary actor associations
UC51 --> ES
UC17 --> FS
UC44 --> FS
UC46 --> FS
UC6 --> FS
UC14 --> DB
UC15 --> DB
UC16 --> DB
UC41 --> DB
UC42 --> DB
UC43 --> DB

' Include relationships
UC8 ..> UC7 : <<include>>
UC14 ..> UC19 : <<include>>
UC14 ..> UC20 : <<include>>
UC14 ..> UC21 : <<include>>
UC15 ..> UC19 : <<include>>
UC15 ..> UC20 : <<include>>
UC15 ..> UC21 : <<include>>
UC41 ..> UC45 : <<include>>
UC46 ..> UC47 : <<include>>

' Extend relationships
UC22 ..> UC8 : <<extend>>
UC25 ..> UC8 : <<extend>>
UC49 ..> UC47 : <<extend>>

@enduml
"""

        # Create temporary file for PlantUML code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as temp_file:
            temp_file.write(plantuml_code)
            temp_file_path = temp_file.name

        try:
            # Generate diagram using PlantUML
            output_path = f"{output_file}.{format_type}"
            
            # Try to use plantuml command if available
            try:
                cmd = ['plantuml', '-t', format_type, '-o', os.path.dirname(output_path), temp_file_path]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                self.stdout.write(self.style.SUCCESS(f'Comprehensive use case diagram generated: {output_path}'))
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback: try using plantuml Python library
                try:
                    import plantuml
                    server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
                    with open(temp_file_path, 'r') as f:
                        plantuml_code = f.read()
                    
                    # Generate diagram
                    diagram = server.processes(plantuml_code)
                    
                    # Save the diagram
                    with open(output_path, 'wb') as f:
                        f.write(diagram)
                    
                    self.stdout.write(self.style.SUCCESS(f'Comprehensive use case diagram generated: {output_path}'))
                except ImportError:
                    self.stdout.write(self.style.ERROR(
                        'PlantUML not available. Please install it:\n'
                        '1. Install Java: https://java.com/download/\n'
                        '2. Download PlantUML: https://plantuml.com/download\n'
                        '3. Or install plantuml Python library: pip install plantuml'
                    ))
                    return
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)

    def generate_simplified_use_case_diagram(self, output_file, format_type):
        """Generate a simplified use case diagram focusing on core features"""
        
        plantuml_code = """@startuml
left to right direction
skinparam packageStyle rectangle
skinparam usecase {
    BackgroundColor LightBlue
    BorderColor DarkBlue
    ArrowColor DarkBlue
}
skinparam actor {
    BackgroundColor LightGreen
    BorderColor DarkGreen
}

' Actors
:Guest User: as GU
:Registered User: as RU
:Admin User: as AU

rectangle "Recipe Share System" {
    package "Core Features" {
        (Browse Recipes) as UC1
        (View Recipe Details) as UC2
        (Create Recipe) as UC3
        (Edit Recipe) as UC4
        (Add to Favorites) as UC5
        (Add Comments) as UC6
    }
    
    package "User Management" {
        (Register) as UC7
        (Login) as UC8
        (Manage Profile) as UC9
        (Manage Users) as UC10
    }
    
    package "Content Management" {
        (Manage Tags) as UC11
        (Manage Ingredients) as UC12
        (Create Blog Posts) as UC13
    }
}

' Guest User
GU --> UC1
GU --> UC2
GU --> UC7
GU --> UC8

' Registered User
RU --> UC1
RU --> UC2
RU --> UC3
RU --> UC4
RU --> UC5
RU --> UC6
RU --> UC9

' Admin User
AU --> UC10
AU --> UC11
AU --> UC12
AU --> UC13

' Include relationships
UC2 ..> UC1 : <<include>>
UC3 ..> UC12 : <<include>>

' Extend relationships
UC5 ..> UC2 : <<extend>>
UC6 ..> UC2 : <<extend>>

@enduml
"""

        # Create temporary file for PlantUML code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as temp_file:
            temp_file.write(plantuml_code)
            temp_file_path = temp_file.name

        try:
            # Generate diagram using PlantUML
            output_path = f"{output_file}_simplified.{format_type}"
            
            try:
                cmd = ['plantuml', '-t', format_type, '-o', os.path.dirname(output_path), temp_file_path]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                self.stdout.write(self.style.SUCCESS(f'Simplified use case diagram generated: {output_path}'))
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    import plantuml
                    server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
                    with open(temp_file_path, 'r') as f:
                        plantuml_code = f.read()
                    
                    diagram = server.processes(plantuml_code)
                    
                    with open(output_path, 'wb') as f:
                        f.write(diagram)
                    
                    self.stdout.write(self.style.SUCCESS(f'Simplified use case diagram generated: {output_path}'))
                except ImportError:
                    self.stdout.write(self.style.ERROR('PlantUML library not available'))
        finally:
            os.unlink(temp_file_path)

    def handle(self, *args, **options):
        output_file = options['output']
        format_type = options['format']
        
        self.stdout.write('🎨 Generating comprehensive use case diagram for Recipe Share app...')
        self.generate_comprehensive_use_case_diagram(output_file, format_type)
        
        self.stdout.write('📋 Generating simplified use case diagram...')
        self.generate_simplified_use_case_diagram(output_file, format_type)
        
        self.stdout.write(self.style.SUCCESS('✅ Use case diagram generation completed!'))
        self.stdout.write(f'📁 Files generated with format: {format_type}')
        self.stdout.write(f'🌐 View PlantUML diagrams at: https://www.plantuml.com/plantuml/uml/')
        
        # Print summary of app features
        self.stdout.write('\n📊 Recipe Share App Features Summary:')
        self.stdout.write('   • User Authentication & Profile Management')
        self.stdout.write('   • Recipe Creation, Editing, and Management')
        self.stdout.write('   • Social Features (Favorites, Comments)')
        self.stdout.write('   • Content Management (Tags, Ingredients)')
        self.stdout.write('   • Blog System')
        self.stdout.write('   • Photo Management')
        self.stdout.write('   • Admin & Staff Management Tools') 