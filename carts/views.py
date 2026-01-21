from django.shortcuts import render , redirect
from django.http import HttpResponse
from store.models import Product
from carts.models import Cart
from carts.models import CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


#to get session id 
# it is private function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request , product_id):
#  to get the product
    product=Product.objects.get(id=product_id)
    try:
        # get the cart using the cart_ID presnet in the sessoion
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

# to put the product inside the cart , product become cartItem and there can be multiple cartItems so 
# combing cart and  product to get cartItem

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  #increase the quantiry with 1 
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart ,

        )
        cart_item.save()
    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect('cart')
        


def cart(request,total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart , is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass # leave it

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total
    }
    return render(request,'store/cart.html',context)