from typing import OrderedDict
from django.contrib import messages
from store.forms import ReviewForm
from django.core import paginator
from django.http import HttpResponse
from carts.models import CartItem
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, ProductGalery, ReviewRating
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from orders.models import OrderProduct

# Create your views here.
def store(request,category_slug=None):
    categories = None 
    products=None

    if category_slug !=None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available=True)
        #Paginator kodu
        paginator = Paginator(products, 3)
        page = request.GET.get('page') #linkdegi ?page=
        paged_products = paginator.get_page(page)

        #product sayi
        product_count = products.count()
        
        
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        #Paginator kodu
        paginator = Paginator(products, 3)
        page = request.GET.get('page') #linkdegi ?page=
        paged_products = paginator.get_page(page)

        #product sayi
        product_count = products.count()


    context = {
        'products':paged_products,
        'product_count':product_count,
        'paged_products':paged_products
        
    }
    return render(request, 'store/store.html', context)


# def product_detail(request, category_slug, product_slug):
#     category = get_object_or_404(Category, slug = category_slug)
#     single_product = get_object_or_404(Product, slug = product_slug, category_id=category.id)
    
#     context=dict(
#     single_product=single_product)
#     return render(request, 'store/product_detail.html',context)


def product_detail(request, category_slug, product_slug):

    
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product = single_product).exists()


        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e
    ################################
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user = request.user, product_id = single_product.id).exists()

        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    #######################################
    #rewiewsi listelemek
    reviews = ReviewRating.objects.filter(product_id = single_product.id, status=True)

    product_galery = ProductGalery.objects.filter(product_id = single_product.id)
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews':reviews,
        'product_galery': product_galery,
    }
    return render(request, 'store/product_detail.html',context)



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')  
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.product_id = product_id
                data.user_id = request.user.id
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()
                messages.success(request, 'Thank you! Your review has been updated.')
                return redirect(url)
            
        


