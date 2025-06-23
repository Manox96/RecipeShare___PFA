from django import forms
from .models import Photo, Recipe, RecipeIngredient, Step, Tag, Blog

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['Nom', 'Descreption', 'image']
        labels = {
            'Nom': 'Nom de la photo',
            'Descreption': 'Description',
            'image': 'Image'
        }
        widgets = {
            'Descreption': forms.Textarea(attrs={'rows': 1}),
        }

class RecipeForm(forms.ModelForm):
    # Add an ImageField for file uploads
    image = forms.ImageField(required=False, label='Recipe Image')
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Tags/Categories'
    )
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'difficulty', 'prep_time', 'cook_time', 
                 'servings', 'cuisine', 'meal_type', 'image', 'is_public', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'required': True}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': True}),
            'difficulty': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'prep_time': forms.NumberInput(attrs={'min': 1, 'class': 'form-control', 'required': True}),
            'cook_time': forms.NumberInput(attrs={'min': 1, 'class': 'form-control', 'required': True}),
            'servings': forms.NumberInput(attrs={'min': 1, 'class': 'form-control', 'required': True}),
            'cuisine': forms.Select(attrs={'class': 'form-select'}),
            'meal_type': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        prep_time = cleaned_data.get('prep_time')
        cook_time = cleaned_data.get('cook_time')
        servings = cleaned_data.get('servings')
        
        if prep_time and prep_time < 1:
            raise forms.ValidationError('Preparation time must be at least 1 minute.')
        
        if cook_time and cook_time < 1:
            raise forms.ValidationError('Cooking time must be at least 1 minute.')
        
        if servings and servings < 1:
            raise forms.ValidationError('Servings must be at least 1.')
        
        return cleaned_data

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'unit', 'quantity']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'unit': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        
        if quantity is not None and quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        
        return cleaned_data

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['step_number', 'instruction']
        widgets = {
            'step_number': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'instruction': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'required': True}),
        }

RecipeIngredientFormSet = forms.inlineformset_factory(
    Recipe, RecipeIngredient,
    form=RecipeIngredientForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True
)

StepFormSet = forms.inlineformset_factory(
    Recipe, Step,
    form=StepForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True
)

class BlogForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=255, 
        required=False,
        help_text='Enter comma-separated tags.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})) 