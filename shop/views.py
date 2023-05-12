from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
# login  Imports
from django.shortcuts import render ,redirect ,HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate ,login , logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

class RegisterViewnew(View) :

    def post(self, request) :
        if request.user.is_authenticated :
            return redirect('shop:product_list')
        else :
            form = CreateUserForm(request.POST)
            if form.is_valid():
                print("User Created")
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request , user +  "  User succesfully created " )
                return redirect("shop:login_page")

            print("At athat ")
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2= request.POST.get('password2')
            if password1 != password2 :
                print("dont match ")
                messages.error(request , "Password doesn't match ")
            elif len(password1)<= 8 :
                messages.error(request , "Password length doesn't match or User already exists  ")

            form = CreateUserForm()
            context = {"form" :form }
            return render(request , "shop/product/register.html" ,context)

    def get(self, request) :
        if request.user.is_authenticated :
            return redirect('shop:product_list')
        else :
            form = CreateUserForm()
            context = {"form" :form }
            return render(request , "shop/product/register.html", context)



class LoginView(View) :

    def get(self,request) :
        if request.user.is_authenticated :
            return redirect('shop:product_list')
        else :
            context ={'form':AuthenticationForm(request)}
            return render(request , "shop/product/login.html" , context)

    def post(self,request) :
        if request.user.is_authenticated :
            return redirect('shop:product_list')
        else :
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request , username=username , password=password)
            if user is not None :
                login(request , user )
                return redirect('shop:product_list')
            else :
                messages.error(request ,"Username Or Password is Incorrect ")
                context ={'form':AuthenticationForm(request)}
                return render(request , "shop/product/login.html" , context)


def logoutUser(request) :
    logout(request)
    return redirect('shop:login_page')

def FAQ(request) :
    return render(request, 'FAQ.html', {})

def About(request) :
    return render(request, 'About.html', {})

def profile(request) :
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your intergalactic account has been updated')
            return redirect('shop:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)



# So whenever you want auth to redirect page just use this decorator
@login_required(login_url="shop:login_page")
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

@login_required(login_url="shop:login_page")
def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

