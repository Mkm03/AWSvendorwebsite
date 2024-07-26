from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Vendor, Product


class CustomSignupForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('vendor', 'Vendor'),
        ('user', 'User'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            role = self.cleaned_data['role']
            can_create = can_edit = (role == 'vendor')
            UserProfile.objects.create(
                user=user,
                role=role,
                can_create=can_create,
                can_edit=can_edit,
                can_view=True
            )
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'can_create', 'can_edit', 'can_view']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'website', 'description']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['vendor', 'name', 'description', 'pdf']


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255, required=False)
    # search_in = forms.ChoiceField(choices=[('vendors', 'Vendors'), ('products', 'Products')], required=True)