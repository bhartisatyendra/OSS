from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from . models import Product, Category, Customer,Orders,ShoppingCart
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')


def productPage(request):
    if request.method == "POST":
        return redirect('product')
    else:
        category_id=request.GET.get('category')
        data = {}
        if category_id:
           products= Product.get_products_by_categoryid(category_id)
        else:
          products = Product.get_all_products()
        category = Category.get_all_category()
        data['products'] = products
        data['category'] = category
        return render(request, 'product.html', data)


def register(request):
    if request.method == 'POST':
        err=None
        name= request.POST.get('name')
        email = request.POST.get('email')
        passwd = request.POST.get('password')
        addr = request.POST.get('address')
        pin = request.POST.get('pincode')
        phone = request.POST.get('phone')
        gen = request.POST.get('gender')

        #Validation
        values={'name':name,
                'email':email,
                'addr':addr,
                'pin':pin,
                'phone':phone,
                'gen':gen,}
        customer = Customer(name=name, gender=gen, address=addr, pincode=pin, contactno=phone, emailaddress=email,
                            password=passwd)

        if not name.isalpha():
            err="Invalid Name, please try again"
        if not phone.isnumeric() or len(phone)<10:
            err="Invalid Contact Number, please try again"
        if not pin.isnumeric():
            err="Invalid Pincode, please try again"
        if customer.is_exists():
            err="Email Already Exists"
        data={}
        data['err']=err
        data['values']=values
        if err:
            return render(request, 'register.html',data)
        #customer.password=make_password(passwd)
        customer.save()
        myuser = User.objects.create_user(username=email,email=email, password=passwd)
        myuser.save()

        err = "You are registered! Try Logging in"
        return render(request, 'login.html',{'err':err})
    else:
        return render(request, 'register.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        myuser = authenticate(username=email, password=password)
        if myuser is not None:
            login(request, myuser)
            try:
                cart=ShoppingCart.objects.filter(customer=Customer.objects.get(emailaddress=request.user.username))
            except Exception as e:
                print(e)
                cart=[]
            request.session['cart']=len(cart)
            return redirect('user')
        else:
            msg="Incorrect Id or password"
            return render(request,'login.html',{'msg':msg})
    return render(request,'login.html')

@login_required(redirect_field_name='login')
def user(request):
    customer = Customer.get_customer_by_email(request.user.username)
    data={}
    if request.method=='POST':
        msg=None
        err=None
        current_password=request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if customer.password==current_password:
            if new_password==confirm_password:
                customer.password=new_password
                customer.save()
                myuser=User.objects.get(username=request.user.username)
                myuser.password=make_password(new_password)
                myuser.save()
                data['msg']='Password Changed Successfully'

            else:
                return render(request, 'changepass.html', {'err': 'New password and confirm password does not match'})
        else:
            return render(request,'changepass.html',{'err':'Incorrect Password'})
    data['customer']=customer
    return render(request,'user.html',data)

@login_required(redirect_field_name='login')
def orders(request):
    orders=Orders.objects.filter(customer=request.user.username).order_by('-order_date')
    return render(request,'orders.html',{'orders':orders})

@login_required(redirect_field_name='login')
def changepass(request):
    return render(request,'changepass.html')

def signout(request):
    logout(request)
    request.session.flush()
    return redirect('index')


@login_required(redirect_field_name='login')
def buynow(request):
    data={}
    if request.method=='GET':
        total=request.GET.get('total')
        if int(total) < 1:
            err="Total cannot be zero"
            return redirect('/mycart/?err='+err)
        method = "add_to_cart"
        customer = Customer.get_customer_by_email(request.user.username)
        cart=ShoppingCart.objects.filter(customer=customer)
        data['cart']=cart

    else:
        method = "buy_now"
        productid=request.POST.get('product')
        #print(productid)
        product=Product.get_product_by_id(productid)
        email=request.user.username
        customer=Customer.get_customer_by_email(email)
        data['product']=product
        data['customer']=customer
    data['method']=method
    return render(request,'confirm.html',data)

@login_required(redirect_field_name='login')
def checkout(request):
    if request.method=='GET':
        customer = Customer.get_customer_by_email(request.user.username)
        cart = ShoppingCart.objects.filter(customer=customer)
        for items in cart:
            order = Orders(customer=items.customer, product=items.product, quantity=items.quantity,
                           price=items.product.price, address=items.customer.address, pincode=items.customer.pincode)
            order.save()
        ShoppingCart.objects.filter(customer=Customer.get_customer_by_email(request.user.username)).delete()
        request.session['cart'] = 0

    else:
        product=Product.get_product_by_id(request.POST.get('productid'))
        customer =Customer.get_customer_by_email(request.POST.get('email'))
        quantity = request.POST.get('quantity')
        order=Orders(customer=customer,product=product,price=product.price,address=customer.address,pincode=customer.pincode,quantity=quantity)
        order.save()

    return render(request,'checkout.html')


@login_required(redirect_field_name='login')
def mycart(request):
    if request.method == "GET" and request.GET.get('flag') == "add_to_cart":
        category=request.GET.get('category')
        product = Product.objects.get(id=request.GET.get('product_id'))
        customer = Customer.get_customer_by_email(request.user.username)
        cart = ShoppingCart(customer=customer, product=product, quantity=1)
        cart.save()
        print(request.session.get('cart'))
        request.session['cart']=request.session.get('cart')+1
        msg="Product Added to Cart"
        #return render(request, 'product.html', {'msg':msg})
        return redirect('/product/?msg='+msg+'&category='+category)
    cart=ShoppingCart.objects.filter(customer=Customer.objects.get(emailaddress=request.user.username))
    total=sum([cartitem.product.price*cartitem.quantity for cartitem in cart])
    return render(request,'mycart.html',{'cart':cart,'total':total})

@login_required(redirect_field_name='login')
def update_cart(request):
    err=None
    if request.method=='POST':
        cart_item_id=request.POST.get('cart_item_id')
        quantity=request.POST.get('quantity')
        if int(quantity) > 0:
            cart=ShoppingCart.objects.get(id=cart_item_id)
            cart.quantity=quantity
            cart.save()
            return redirect('mycart')
        else:
            err="Quantity cannot be less than 1"
    elif request.method=='GET' and request.GET.get('cart_item'):
        cart_item_id=request.GET.get('cart_item')
        try:
            ShoppingCart.objects.get(id=cart_item_id).delete()
            request.session['cart'] = request.session.get('cart') -1
        except Exception as e:
            print(e)
            pass
    else:
        try:
            ShoppingCart.objects.filter(customer=Customer.get_customer_by_email(request.user.username)).delete()
            request.session['cart'] = 0
            err="Cart Empty"
        except Exception as e:
            pass
    if err:
        return redirect('/mycart/?err='+err)
    else:
        return redirect('/mycart/')