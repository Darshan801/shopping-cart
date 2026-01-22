from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse
from django.db.models import Q
import sys
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None
    
    #for filter by  category
    if category_slug != None:
        categories=get_object_or_404(Category, slug=category_slug) # bring 404 error when categories isnot found
        products=Product.objects.filter(category=categories ,is_available=True)
        paginator = Paginator(products, 6) #to show 6 products in a page
        page = request.GET.get('page') # getting page no using get request
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else: # for all category
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6) #to show 6 products in a page
        page = request.GET.get('page') # getting page no using get request
        paged_products = paginator.get_page(page)
        product_count = products.count()




    context = {
        'products': paged_products,
        'product_count':product_count,
        # 'paged_products':paged_products,
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

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # filtering on the basis of product_name and description, if it contains the keyword it will show the product
            products = Product.objects.filter(
                Q(product_name__icontains=keyword) | 
                Q(description__icontains=keyword)
            ).order_by('-created_date')
            product_count = products.count()
            context={
                'products':products,
                'product_count':product_count
            }
    return render(request,'store/store.html',context)