from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import modelformset_factory
from .models import CustomUser, House, HouseImage

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'style': 'border-radius:8px; padding:10px;'
        })
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number',
            'style': 'border-radius:8px; padding:10px;'
        })
    )
    role = forms.ChoiceField(
        choices=[('tenant', 'Tenant'), ('landlord', 'Landlord'), ('manager', 'Manager')],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'style': 'border-radius:8px; padding:10px; background-color:#fdf2f8;'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'style': 'border-radius:8px; padding:10px;'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'style': 'border-radius:8px; padding:10px;'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'role', 'password1', 'password2']


class HouseForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(
        required=True,
        label="I agree to the listing terms and conditions",
        error_messages={'required': 'You must agree to the terms to continue.'},
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'style': 'margin-right:10px;'
        })
    )

    class Meta:
        model = House
        fields = ['title', 'location', 'description', 'latitude', 'longitude', 'price']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter house title',
                'style': 'border-radius:8px; padding:10px;'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location',
                'style': 'border-radius:8px; padding:10px;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the house...',
                'rows': 4,
                'style': 'border-radius:8px; padding:10px;'
            }),
            'latitude': forms.TextInput(attrs={
                'readonly': 'readonly',
                'placeholder': 'Click on the map to set latitude',
                'class': 'form-control',
                'style': 'background-color:#f0f0f0; border-radius:8px; padding:10px;'
            }),
            'longitude': forms.TextInput(attrs={
                'readonly': 'readonly',
                'placeholder': 'Click on the map to set longitude',
                'class': 'form-control',
                'style': 'background-color:#f0f0f0; border-radius:8px; padding:10px;'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price in KES',
                'style': 'border-radius:8px; padding:10px;'
            }),
        }


HouseImageFormSet = modelformset_factory(
    HouseImage,
    fields=('image', 'caption'),
    extra=3,
    widgets={
        'image': forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'style': 'border-radius:8px; padding:10px; background-color:#f0f9ff;'
        }),
        'caption': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter image caption',
            'style': 'border-radius:8px; padding:10px;'
        }),
    }
)