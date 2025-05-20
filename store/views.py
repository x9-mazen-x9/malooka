from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
import urllib.parse
from .models import Product, Order, SiteVisit, ProductImage

# تسجيل الزيارة اليومية
def record_visit():
    today = timezone.now().date()
    visit, created = SiteVisit.objects.get_or_create(date=today)
    visit.count += 1
    visit.save()

# حساب عدد العناصر في السلة
def get_cart_count(request):
    cart = request.session.get('cart', {})
    return sum(item['quantity'] for item in cart.values())

# عرض قائمة المنتجات مع إمكانية البحث
def product_list(request):
    record_visit()
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    cart_count = get_cart_count(request)  # ← عدد المنتجات في السلة

    return render(request, 'store/product_list.html', {
        'products': products,
        'cart_count': cart_count  # ← نرسله للتمبلت
    })

# عرض تفاصيل منتج
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = ProductImage.objects.filter(product=product)
    cart_count = get_cart_count(request)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'images': images,
        'cart_count': cart_count
    })

# إضافة منتج إلى السلة
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        cart[str(pk)]['quantity'] += 1
    else:
        cart[str(pk)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else ''
        }

    request.session['cart'] = cart
    return redirect('product_list')

# عرض السلة
def view_cart(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    cart_count = get_cart_count(request)

    return render(request, 'store/cart.html', {
        'cart': cart,
        'total_price': total_price,
        'cart_count': cart_count
    })

# إزالة منتج من السلة
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
    return redirect('view_cart')

# مسح السلة بالكامل
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('view_cart')

# تأكيد الطلب وتحويل للواتساب
def confirm_order(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        name = request.POST['full_name']
        address = request.POST['address']
        phone = request.POST['phone']
        order_time = timezone.now()

        Order.objects.create(
            full_name=name,
            address=address,
            phone=phone,
            product=product,
            order_time=order_time
        )

        message = f"السلام عليكم، عايز اطلب {product.name}"
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/201234567890?text={encoded_message}"

        return HttpResponseRedirect(whatsapp_url)

    images = ProductImage.objects.filter(product=product)
    cart_count = get_cart_count(request)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'images': images,
        'cart_count': cart_count
    })
