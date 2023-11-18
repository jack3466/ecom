from django.shortcuts import render,redirect
from django.http import HttpResponse
from startapp.models import Product,Cart,Buy
# Create your views here.
from startapp.forms import CartForm
from startapp.startapp import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm


def index(request):
    p=Product.objects.all()
    if request.GET.get('q'):
        query=request.GET.get('q')
        p=Product.objects.filter(title__contains=query)
    context={'p':p}
    return render(request,'index.html',context)
@login_required
def detail(request,product_id,slug):
    d=Product.objects.get(id=product_id)
    if request.method=="POST":
        f=CartForm(request,request.POST)
        if f.is_valid():
            request.form_data=f.cleaned_data
            add_to_cart(request)
            #return HttpResponse('added to cart')
            return redirect('startapp:cart_view')
    f=CartForm(request,initial={'product_id':product_id})
    context={'d':d,'f':f}
    return render(request,'detail.html',context)
@login_required
def cart_view(request):
    if request.method=='POST' and request.POST.get('delete')=='delete':
        item_id=request.POST.get('item_id')
        cd=Cart.objects.get(id=item_id)
        cd.delete()
    c=get_cart(request)
    t=total(request)
    co=item_count(request)
    context={'c':c,'t':t}
    return render(request,'cart.html',context)
@login_required
def order(request):


    # What you want the button to do.
    items=get_cart(request)
    for i in items:
        b=Buy(Product_id=i.product_id,quantity=i.quantity,price=i.price)
        b.save()
    paypal_dict = {
        "business": "sb-6ivrx28145946@business.example.com",
        "amount": total(request),
        "item_name": cart_id(request),
        "invoice": str(
            ()),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('startapp:return_view')),
        "cancel_return": request.build_absolute_uri(reverse('startapp:cancel_view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form,"items":items,"total":total(request)}
    return render(request, "order.html", context)
@login_required
def return_view(request):
    return HttpResponse('transaction success')
@login_required
def cancel_view(request):
    return HttpResponse('transaction canceled   ....go to school....')