from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import modelformset_factory
from .models import CustomUser, House, HouseImage

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'role', 'password1', 'password2']

class HouseForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(
        required=True,
        label="I agree to the listing terms and conditions",
        error_messages={'required': 'You must agree to the terms to continue.'}
    )

    class Meta:
        model = House
        fields = ['title', 'location', 'description', 'latitude', 'longitude', 'price']
        widgets = {
            'latitude': forms.TextInput(attrs={
                'readonly': 'readonly',
                'placeholder': 'Click on the map to set latitude',
                'style': 'background-color:#f0f0f0;'
            }),
            'longitude': forms.TextInput(attrs={
                'readonly': 'readonly',
                'placeholder': 'Click on the map to set longitude',
                'style': 'background-color:#f0f0f0;'
            }),
        }

HouseImageFormSet = modelformset_factory(
    HouseImage,
    fields=('image', 'caption'),
    extra=3,  # You can increase this number to allow more uploads
)