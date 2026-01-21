from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse
import sys
# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None
    
    if category_slug != None:
        categories=get_object_or_404(Category, slug=category_slug) # bring 404 error when categories isnot found
        products=Product.objects.filter(category=categories ,is_available=True)
        product_count=products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()




    context = {
        'products': products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)

def product_detail(request, category_slug, product_slug):
   
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug) #category__slug is basically a syntax double underscore used to access related foregin key
        
         # if it exists it shows true if false then product isnot in cart
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists() # cart is used as foregin key in Cart model
        
    except Exception as e:
        raise e
    
    context={
        'single_product':single_product,
        'in_cart':in_cart,
    }
    return render(request,'store/product_detail.html',context)