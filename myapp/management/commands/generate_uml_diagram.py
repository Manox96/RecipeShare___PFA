from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Recipe, Blog, Tag, Ingredient, Cuisine, MealType
import os
import subprocess
import tempfile

class Command(BaseCommand):
    help = 'Generates use case UML diagrams for the Recipe Share System'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='uml_diagram',
            help='Output filename (without extension)'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['png', 'svg', 'pdf'],
            default='png',
            help='Output format'
        )

    def generate_use_case_diagram(self, output_file, format_type):
        """Generate a comprehensive use case diagram for the Recipe Share System"""
        
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
:Staff Member: as SM
:Email System: as ES
:File System: as FS

rectangle "Recipe Share System" {
    package "Authentication & User Management" {
        (Register Account) as UC1
        (Login) as UC2
        (Logout) as UC3
        (View Profile) as UC4
        (Update Profile) as UC5
    }
    
    package "Recipe Management" {
        (Browse Public Recipes) as UC6
        (View Recipe Details) as UC7
        (Create Recipe) as UC8
        (Edit Recipe) as UC9
        (Delete Recipe) as UC10
        (Add to Favorites) as UC11
        (View Favorites) as UC12
        (Add Comment) as UC13
    }
    
    package "Content Management" {
        (Manage Users) as UC14
        (Manage Tags) as UC15
        (Manage Ingredients) as UC16
        (Manage Cuisines) as UC17
        (Manage Meal Types) as UC18
    }
    
    package "Blog System" {
        (View Blog Posts) as UC19
        (Create Blog Post) as UC20
        (Edit Blog Post) as UC21
        (Delete Blog Post) as UC22
    }
    
    package "Communication" {
        (Contact Support) as UC23
    }
}

' Guest User associations
GU --> UC1
GU --> UC2
GU --> UC6
GU --> UC7
GU --> UC19
GU --> UC23

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
RU --> UC19
RU --> UC23

' Admin User associations
AU --> UC14
AU --> UC20
AU --> UC21
AU --> UC22
AU --> UC23

' Staff Member associations
SM --> UC15
SM --> UC16
SM --> UC17
SM --> UC18

' Secondary actor associations
UC23 --> ES
UC8 --> FS
UC20 --> FS

' Include relationships
UC7 ..> UC6 : <<include>>
UC8 ..> UC16 : <<include>>
UC8 ..> UC15 : <<include>>
UC20 ..> UC15 : <<include>>

' Extend relationships
UC11 ..> UC7 : <<extend>>
UC13 ..> UC7 : <<extend>>

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
                self.stdout.write(self.style.SUCCESS(f'Diagram generated successfully: {output_path}'))
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
                    
                    self.stdout.write(self.style.SUCCESS(f'Diagram generated successfully: {output_path}'))
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

    def generate_system_overview_diagram(self, output_file, format_type):
        """Generate a system overview diagram"""
        
        plantuml_code = """@startuml
!define RECTANGLE class

package "Recipe Share System" {
    package "User Management" {
        [User] as User
        [Profile] as Profile
        [Authentication] as Auth
    }
    
    package "Recipe System" {
        [Recipe] as Recipe
        [Ingredient] as Ingredient
        [Step] as Step
        [Cuisine] as Cuisine
        [MealType] as MealType
        [Difficulty] as Difficulty
        [Tag] as Tag
    }
    
    package "Social Features" {
        [Favorite] as Favorite
        [Comment] as Comment
    }
    
    package "Blog System" {
        [Blog] as Blog
        [BlogTag] as BlogTag
    }
    
    package "File Management" {
        [RecipeImage] as RecipeImage
        [BlogImage] as BlogImage
    }
}

' Relationships
User ||--o{ Recipe : creates
User ||--o{ Blog : creates
User ||--o{ Favorite : has
User ||--o{ Comment : makes
User ||--|| Profile : has

Recipe ||--o{ Ingredient : contains
Recipe ||--o{ Step : has
Recipe ||--o{ Tag : tagged_with
Recipe ||--|| Cuisine : belongs_to
Recipe ||--|| MealType : is_type
Recipe ||--|| Difficulty : has
Recipe ||--o{ RecipeImage : has

Blog ||--o{ BlogTag : tagged_with
Blog ||--o{ BlogImage : has

@enduml
"""

        # Create temporary file for PlantUML code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as temp_file:
            temp_file.write(plantuml_code)
            temp_file_path = temp_file.name

        try:
            # Generate diagram using PlantUML
            output_path = f"{output_file}_system_overview.{format_type}"
            
            try:
                cmd = ['plantuml', '-t', format_type, '-o', os.path.dirname(output_path), temp_file_path]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                self.stdout.write(self.style.SUCCESS(f'System overview diagram generated: {output_path}'))
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    import plantuml
                    server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
                    with open(temp_file_path, 'r') as f:
                        plantuml_code = f.read()
                    
                    diagram = server.processes(plantuml_code)
                    
                    with open(output_path, 'wb') as f:
                        f.write(diagram)
                    
                    self.stdout.write(self.style.SUCCESS(f'System overview diagram generated: {output_path}'))
                except ImportError:
                    self.stdout.write(self.style.ERROR('PlantUML library not available'))
        finally:
            os.unlink(temp_file_path)

    def generate_simple_example_diagram(self, output_file, format_type):
        """Generate a simple example diagram like the one from the documentation"""
        
        plantuml_code = """@startuml
left to right direction
skinparam packageStyle rectangle

:Food Critic: as fc
:Restaurant Staff: as rs

rectangle Restaurant {
    (Eat Food) as UC1
    (Pay for Food) as UC2
    (Drink) as UC3
    (Order Food) as UC4
    (Prepare Food) as UC5
}

fc --> UC1
fc --> UC2
fc --> UC3
fc --> UC4
rs --> UC5

UC4 ..> UC5 : <<include>>
UC1 ..> UC2 : <<extend>>

@enduml
"""

        # Create temporary file for PlantUML code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as temp_file:
            temp_file.write(plantuml_code)
            temp_file_path = temp_file.name

        try:
            # Generate diagram using PlantUML
            output_path = f"{output_file}_simple_example.{format_type}"
            
            try:
                cmd = ['plantuml', '-t', format_type, '-o', os.path.dirname(output_path), temp_file_path]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                self.stdout.write(self.style.SUCCESS(f'Simple example diagram generated: {output_path}'))
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    import plantuml
                    server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
                    with open(temp_file_path, 'r') as f:
                        plantuml_code = f.read()
                    
                    diagram = server.processes(plantuml_code)
                    
                    with open(output_path, 'wb') as f:
                        f.write(diagram)
                    
                    self.stdout.write(self.style.SUCCESS(f'Simple example diagram generated: {output_path}'))
                except ImportError:
                    self.stdout.write(self.style.ERROR('PlantUML library not available'))
        finally:
            os.unlink(temp_file_path)

    def handle(self, *args, **options):
        output_file = options['output']
        format_type = options['format']
        
        self.stdout.write('Generating use case UML diagram...')
        self.generate_use_case_diagram(output_file, format_type)
        
        self.stdout.write('Generating system overview diagram...')
        self.generate_system_overview_diagram(output_file, format_type)
        
        self.stdout.write('Generating simple example diagram...')
        self.generate_simple_example_diagram(output_file, format_type)
        
        self.stdout.write(self.style.SUCCESS('UML diagram generation completed!'))
        self.stdout.write(f'Files generated with format: {format_type}')
        self.stdout.write(f'You can view PlantUML diagrams at: https://www.plantuml.com/plantuml/uml/') 