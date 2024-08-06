from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
import razorpay
from .models import Product,Customer,Cart
from .forms import CustomerRegisterationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings


# Create your views here.
def home(request):
    return render(request,"app/home.html")

def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")

def refundpolicy(request):
    return render(request,"app/refundpolicy.html")

def privacypolicy(request):
    return render(request,"app/privacypolicy.html")

def terms(request):
    return render(request,"app/terms.html")

class CategoryView(View):
    def get(self,request,val):
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values
        return render(request,"app/category.html",locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
class ProductDetail(View):
    def get(self,request,pk):
       product=Product.objects.get(pk=pk)
       return render(request,"app/productdetail.html",locals()) 
    
class CustomerRegisterationView(View):
    def get(self,request):
        form=CustomerRegisterationForm()
        return render(request,'app/customerregisteration.html',locals())
    
    def post(self,request):
        form=CustomerRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registeration sucessfull !!!")
        else:
            messages.warning(request,"Invalid data")
        return render(request,'app/customerregisteration.html',locals())
    



class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm
        return render(request,"app/profile.html",locals()) 
    
    def post(self, request):
        if request.method == 'POST':
            form = CustomerProfileForm(request.POST)
            if form.is_valid():
                user = request.user
                name = form.cleaned_data['name']
                locality = form.cleaned_data['locality']
                city = form.cleaned_data['city']
                mobile = form.cleaned_data['mobile']
                state = form.cleaned_data['state']
                zipcode = form.cleaned_data['zipcode']

                reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
                reg.save()
                messages.success(request, 'Profile saved Successfully !!!')
            else:
                messages.warning(request, 'Invalid data')
        else:
            form = CustomerProfileForm()

        return render(request, "app/profile.html", {'form': form})

def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

class UpdateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,'app/updateaddress.html',locals())
    def post(self,request,pk): 
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'Address updated Successfully !!!')
        else:
            messages.warning(request, 'Invalid data')
        return redirect("address")
    

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount=amount+value
        totalamount=amount+40
    return render(request,'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity * p.product.discounted_price
            famount= value + famount
        totalamount=famount + 40
        razoramount=int(totalamount*100)
        #client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        #data={"amount" : razoramount, "currency": "INR", "receipt":"order_rcptid_12"}
        #payment_response=client.order.create(data=data)
        #print(payment_response)
        return render(request,'app/checkout.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            product = Product.objects.get(id=prod_id)
            cart_item = Cart.objects.filter(Q(product=product) & Q(user=request.user)).first()
            if cart_item:
                cart_item.quantity += 1
                cart_item.save()

                # Calculate the total amount
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = sum(p.quantity * p.product.discounted_price for p in cart)
                totalamount = amount + 40

                data = {
                    'quantity': cart_item.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item not found'}, status=404)

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            product = Product.objects.get(id=prod_id)
            cart_item = Cart.objects.filter(Q(product=product) & Q(user=request.user)).first()
            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()

                # Calculate the total amount
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = sum(p.quantity * p.product.discounted_price for p in cart)
                totalamount = amount + 40

                data = {
                    'quantity': cart_item.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item not found'}, status=404)

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            product = Product.objects.get(id=prod_id)
            cart_item = Cart.objects.filter(Q(product=product) & Q(user=request.user)).first()
            if cart_item:
                if cart_item:
                    cart_item.delete()

                # Calculate the total amount
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = sum(p.quantity * p.product.discounted_price for p in cart)
                totalamount = amount + 40

                data = {
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item not found'}, status=404)

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
