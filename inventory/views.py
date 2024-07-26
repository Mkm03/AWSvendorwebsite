from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm, VendorForm, ProductForm, UserUpdateForm, UserProfileForm, SearchForm
from .models import UserProfile, Vendor, Product
from django.db import IntegrityError


def sign_up(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure UserProfile is created
            try:
                UserProfile.objects.create(
                    user=user,
                    role=form.cleaned_data.get('role'),
                    can_create=(form.cleaned_data.get('role') == 'vendor'),
                    can_edit=(form.cleaned_data.get('role') == 'vendor'),
                    can_view=True
                )
            except IntegrityError:
                # If the profile already exists, handle it gracefully
                pass
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = CustomSignupForm()
    return render(request, 'inventory/sign_up.html', {'form': form})


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    is_vendor = request.user.userprofile.role == 'vendor'
    vendors = Vendor.objects.filter(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    return render(request, 'inventory/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_vendor': is_vendor,
        'vendors': vendors
    })


@login_required
def create_vendor(request):
    if request.user.userprofile.role != 'vendor':
        return redirect('vendor_list')

    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.save()
            return redirect('profile')
    else:
        form = VendorForm()

    return render(request, 'inventory/vendor_form.html', {'form': form})


@login_required
def update_vendor(request, pk):
    if request.user.userprofile.role != 'vendor':
        return redirect('vendor_list')
    vendor = get_object_or_404(Vendor, pk=pk, user=request.user)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'inventory/vendor_form.html', {'form': form})

@login_required
def delete_vendor(request, pk):
    if request.user.userprofile.role != 'vendor':
        return redirect('vendor_list')
    vendor = get_object_or_404(Vendor, pk=pk, user=request.user)
    vendor.delete()
    return redirect('profile')

@login_required
def vendor_list(request):
    vendors = Vendor.objects.all()
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        if query:
            vendors = vendors.filter(name__icontains=query)
    return render(request, 'inventory/vendor_list.html', {
        'vendors': vendors,
        'search_form': search_form,
    })


@login_required
def create_product(request):
    if request.user.userprofile.role != 'vendor':
        return redirect('product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = Vendor.objects.filter(user=request.user).first()
            product.save()
            return redirect('profile')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})


@login_required
def product_list(request):
    products = Product.objects.all()
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        if query:
            products = products.filter(name__icontains=query)
    return render(request, 'inventory/product_list.html', {'products': products, 'search_form': search_form})


@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('profile')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})

@login_required
def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    products = Product.objects.filter(vendor=vendor)
    return render(request, 'inventory/vendor_detail.html', {'vendor': vendor, 'products': products})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory/product_detail.html', {'product': product})


@login_required
def home(request):
    vendors = Vendor.objects.all()
    products = Product.objects.all()
    return render(request, 'inventory/home.html', {'vendors': vendors, 'products': products})
