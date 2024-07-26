from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, Vendor, Product
from .forms import CustomSignupForm, VendorForm
from django.urls import reverse

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.vendor = Vendor.objects.create(user=self.user, name='Test Vendor', website='https://testvendor.com', description='Test Description')

    def test_userprofile_creation(self):
        profile = UserProfile.objects.create(user=self.user, role='vendor')
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.role, 'vendor')

    def test_vendor_creation(self):
        self.assertEqual(self.vendor.name, 'Test Vendor')
        self.assertEqual(self.vendor.website, 'https://testvendor.com')
        self.assertEqual(self.vendor.user.username, 'testuser')

    def test_product_creation(self):
        product = Product.objects.create(vendor=self.vendor, name='Test Product', description='Test Product Description')
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.vendor.name, 'Test Vendor')

class FormTests(TestCase):
    def test_valid_signup_form(self):
        form_data = {'username': 'newuser', 'email': 'user@example.com', 'password': 'strongpassword', 'role': 'vendor'}
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_signup_form(self):
        form_data = {'username': '', 'email': 'invalidemail', 'password': 'pwd', 'role': 'vendor'}
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_vendor_form(self):
        form_data = {'name': 'New Vendor', 'website': 'https://newvendor.com', 'description': 'Vendor Description'}
        form = VendorForm(data=form_data)
        self.assertTrue(form.is_valid())

class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.vendor = Vendor.objects.create(user=self.user, name='Test Vendor', website='https://testvendor.com', description='Test Description')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/home.html')

    def test_vendor_list_view(self):
        response = self.client.get(reverse('vendor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/vendor_list.html')
        self.assertContains(response, 'Test Vendor')

class IntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, role='vendor')
        self.client.login(username='testuser', password='12345')
        self.vendor_data = {'name': 'Integration Vendor', 'website': 'https://integrationvendor.com', 'description': 'Integration Description'}

    def test_vendor_product_workflow(self):
        # Create vendor
        response = self.client.post(reverse('create_vendor'), data=self.vendor_data)
        self.assertEqual(response.status_code, 302)  # Redirects to profile
        vendor = Vendor.objects.get(name='Integration Vendor')
        self.assertIsNotNone(vendor)

        # Add product to vendor
        product_data = {'vendor': vendor.id, 'name': 'Integration Product', 'description': 'Product Description'}
        response = self.client.post(reverse('create_product'), data=product_data)
        self.assertEqual(response.status_code, 302)  # Redirects to profile
        product = Product.objects.get(name='Integration Product')
        self.assertIsNotNone(product)
        self.assertEqual(product.vendor, vendor)
