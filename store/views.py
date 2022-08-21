from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def all_products(request):
    products = Product.products.all()
    return render(request, 'store/index.html', {'products':products})



def product_details(request, slug):
    product_details = get_object_or_404(Product, slug=slug, in_stock=True)

    return render(request, 'store/details.html', {'product_details':product_details})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category_products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {'category':category, 'category_products':category_products})

