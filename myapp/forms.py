from django import forms
from django.contrib.auth.models import User
from .models import Photo, Recipe, RecipeIngredient, Step, Tag, Blog, Profile, BlogComment

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
            'ingredient': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'e.g., 2.5',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].empty_label = "Select ingredient..."
        self.fields['unit'].empty_label = "Select unit..."

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
            'step_number': forms.HiddenInput(),
            'instruction': forms.Textarea(attrs={
                'rows': 2, 
                'class': 'form-control', 
                'placeholder': 'e.g., Mix flour and eggs...'
            }),
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
        help_text='Enter comma-separated tags (e.g., Cooking, Tips, Healthy).',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas...'
        })
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we're editing an existing blog, populate the tags field
        if self.instance and self.instance.pk:
            existing_tags = self.instance.tags.all()
            if existing_tags:
                tag_names = [tag.name for tag in existing_tags]
                self.fields['tags'].initial = ', '.join(tag_names)

    def save(self, commit=True):
        blog = super().save(commit=False)
        if commit:
            blog.save()
            # Clear existing tags and add new ones
            blog.tags.clear()
            tag_names = self.cleaned_data.get('tags', '').strip()
            if tag_names:
                for tag_name in tag_names.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        blog.tags.add(tag)
        return blog

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts...',
                'style': 'resize: vertical;'
            }),
        }
        labels = {
            'comment': 'Your Comment'
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError('Passwords do not match.')
            if password1 and len(password1) < 8:
                raise forms.ValidationError('Password must be at least 8 characters long.')
        return cleaned_data 