from cgi import test
import re
from urllib import response
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import Product
from django.http import JsonResponse
from .cart import Cart

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html',{'cart':cart})

def cart_add( request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
      
        
        product = get_object_or_404(Product, id =product_id)
        cart.add(product=product, qty=product_qty)
        cartquantity = cart.__len__()
        response = JsonResponse({'qty':cartquantity})
        return response

def cart_delete( request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('productid')
        cart.delete(product=product_id)

        cartqty=cart.__len__()
        carttotal = cart.get_total_price()
        response = JsonResponse({'qty':cartqty, 'subtotal':carttotal})
        return response