#!/usr/bin/env python3
"""
Example script demonstrating how to generate UML diagrams using Python libraries.
This script shows different approaches for creating use case diagrams.
"""

import json
import os
import tempfile
import subprocess

def create_simple_plantuml_diagram():
    """Create a simple PlantUML use case diagram using proper syntax"""
    
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
    
    # Save PlantUML code to file
    with open('restaurant_use_case.puml', 'w') as f:
        f.write(plantuml_code)
    
    print("✅ PlantUML diagram saved as 'restaurant_use_case.puml'")
    print("   You can view it at: https://www.plantuml.com/plantuml/uml/")
    
    return plantuml_code

def create_drawio_diagram():
    """Create a draw.io compatible diagram"""
    
    # Simple draw.io diagram structure
    diagram_data = {
        "diagram": {
            "mxGraphModel": {
                "root": {
                    "mxCell": [
                        {"id": "0"},
                        {"id": "1", "parent": "0"},
                        # System boundary
                        {
                            "id": "system",
                            "value": "Restaurant System",
                            "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8f9fa;strokeColor=#6c757d;fontSize=14;fontStyle=1;",
                            "vertex": "1",
                            "parent": "1",
                            "geometry": {
                                "x": 200,
                                "y": 100,
                                "width": 400,
                                "height": 300
                            }
                        },
                        # Actor
                        {
                            "id": "actor",
                            "value": "Food Critic",
                            "style": "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;",
                            "vertex": "1",
                            "parent": "1",
                            "geometry": {
                                "x": 50,
                                "y": 200,
                                "width": 30,
                                "height": 60
                            }
                        },
                        # Use cases
                        {
                            "id": "uc1",
                            "value": "Eat Food",
                            "style": "ellipse;whiteSpace=wrap;html=1;",
                            "vertex": "1",
                            "parent": "system",
                            "geometry": {
                                "x": 250,
                                "y": 150,
                                "width": 100,
                                "height": 50
                            }
                        },
                        {
                            "id": "uc2",
                            "value": "Pay for Food",
                            "style": "ellipse;whiteSpace=wrap;html=1;",
                            "vertex": "1",
                            "parent": "system",
                            "geometry": {
                                "x": 400,
                                "y": 150,
                                "width": 100,
                                "height": 50
                            }
                        },
                        # Association
                        {
                            "id": "edge1",
                            "style": "endArrow=none;html=1;",
                            "edge": "1",
                            "parent": "1",
                            "source": "actor",
                            "target": "uc1",
                            "geometry": {
                                "relative": "1"
                            }
                        },
                        {
                            "id": "edge2",
                            "style": "endArrow=none;html=1;",
                            "edge": "1",
                            "parent": "1",
                            "source": "actor",
                            "target": "uc2",
                            "geometry": {
                                "relative": "1"
                            }
                        }
                    ]
                }
            }
        }
    }
    
    # Save as draw.io file
    with open('restaurant_diagram.drawio', 'w') as f:
        json.dump(diagram_data, f, indent=2)
    
    print("✅ Draw.io diagram saved as 'restaurant_diagram.drawio'")
    print("   You can open it at: https://app.diagrams.net/")
    
    return diagram_data

def create_recipe_system_diagram():
    """Create a comprehensive recipe system use case diagram using proper PlantUML syntax"""
    
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

rectangle "Recipe Share System" {
    package "Authentication" {
        (Register Account) as UC1
        (Login) as UC2
        (Logout) as UC3
    }
    
    package "Recipe Management" {
        (Browse Recipes) as UC4
        (View Recipe Details) as UC5
        (Create Recipe) as UC6
        (Edit Recipe) as UC7
        (Delete Recipe) as UC8
        (Add to Favorites) as UC9
    }
    
    package "Content Management" {
        (Manage Users) as UC10
        (Manage Tags) as UC11
        (Manage Ingredients) as UC12
    }
    
    package "Blog System" {
        (View Blog Posts) as UC13
        (Create Blog Post) as UC14
    }
}

' Guest User associations
GU --> UC1
GU --> UC2
GU --> UC4
GU --> UC5
GU --> UC13

' Registered User associations
RU --> UC3
RU --> UC4
RU --> UC5
RU --> UC6
RU --> UC7
RU --> UC8
RU --> UC9
RU --> UC13

' Admin User associations
AU --> UC10
AU --> UC14

' Staff Member associations
SM --> UC11
SM --> UC12

' Include relationships
UC5 ..> UC4 : <<include>>
UC6 ..> UC12 : <<include>>

' Extend relationships
UC9 ..> UC5 : <<extend>>

@enduml
"""
    
    # Save PlantUML code to file
    with open('recipe_system_use_case.puml', 'w') as f:
        f.write(plantuml_code)
    
    print("✅ Recipe system PlantUML diagram saved as 'recipe_system_use_case.puml'")
    
    return plantuml_code

def create_business_use_case_diagram():
    """Create a business use case diagram example"""
    
    plantuml_code = """@startuml
left to right direction
skinparam packageStyle rectangle

' Business actors (note the / suffix)
:Customer:/ as cust
:Manager:/ as mgr

rectangle "Business System" {
    ' Business use cases (note the / suffix)
    (Process Order)/ as UC1
    (Generate Report)/ as UC2
    (Manage Inventory)/ as UC3
}

cust --> UC1
mgr --> UC2
mgr --> UC3

UC1 ..> UC3 : <<include>>
@enduml
"""
    
    # Save PlantUML code to file
    with open('business_use_case.puml', 'w') as f:
        f.write(plantuml_code)
    
    print("✅ Business use case diagram saved as 'business_use_case.puml'")
    
    return plantuml_code

def try_generate_png():
    """Try to generate PNG from PlantUML if plantuml is available"""
    
    try:
        import plantuml
        
        # Create a simple diagram using proper syntax
        plantuml_code = """@startuml
:User: as u
rectangle System {
    (Do Something) as UC1
}
u --> UC1
@enduml
"""
        
        # Generate PNG using plantuml library
        server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
        diagram = server.processes(plantuml_code)
        
        # Save the PNG
        with open('simple_diagram.png', 'wb') as f:
            f.write(diagram)
        
        print("✅ PNG diagram generated as 'simple_diagram.png'")
        return True
        
    except ImportError:
        print("⚠️  PlantUML library not installed. Install with: pip install plantuml")
        return False
    except Exception as e:
        print(f"❌ Error generating PNG: {e}")
        return False

def main():
    """Main function to demonstrate all diagram generation methods"""
    
    print("🎨 UML Diagram Generation Examples")
    print("=" * 40)
    
    # Create simple restaurant diagram
    print("\n1. Creating simple restaurant use case diagram...")
    create_simple_plantuml_diagram()
    
    # Create draw.io diagram
    print("\n2. Creating draw.io compatible diagram...")
    create_drawio_diagram()
    
    # Create comprehensive recipe system diagram
    print("\n3. Creating comprehensive recipe system diagram...")
    create_recipe_system_diagram()
    
    # Create business use case diagram
    print("\n4. Creating business use case diagram...")
    create_business_use_case_diagram()
    
    # Try to generate PNG
    print("\n5. Attempting to generate PNG diagram...")
    try_generate_png()
    
    print("\n" + "=" * 40)
    print("📋 Summary of generated files:")
    print("   - restaurant_use_case.puml (PlantUML format)")
    print("   - restaurant_diagram.drawio (Draw.io format)")
    print("   - recipe_system_use_case.puml (Comprehensive PlantUML)")
    print("   - business_use_case.puml (Business use case example)")
    print("   - simple_diagram.png (PNG image, if PlantUML available)")
    
    print("\n🔧 To use these diagrams:")
    print("   - PlantUML files: Visit https://www.plantuml.com/plantuml/uml/")
    print("   - Draw.io files: Visit https://app.diagrams.net/")
    print("   - Install PlantUML: pip install plantuml")
    
    print("\n🚀 To run Django management commands:")
    print("   python manage.py generate_uml_diagram")
    print("   python manage.py generate_drawio_diagram")
    
    print("\n📚 PlantUML Documentation:")
    print("   - Use Case Diagrams: https://plantuml.com/use-case-diagram")

if __name__ == "__main__":
    main() 