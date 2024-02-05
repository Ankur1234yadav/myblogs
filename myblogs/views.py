from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Blog_Category, contact_info, subscription,blog_post
from.form import Blog_Form
from.form import BlogPost_Form
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    # return HttpResponse('<h1>This is My Home Page </h1>')
    #fetch the data from db
    x=Blog_Category.objects.all()
    print (x)
    return render(request,"myblogs/home.html",{"category":x})

def findproduct(request):
    if request.method == 'POST':
        x = request.POST.get('prod_search')
        # print(x)
        mydata = Blog_Category.objects.filter(Q(blog_cat__icontains = x) | Q(blog_cat__icontains = x))
        # print(mydata)
        if mydata:
            return render(request,"myblogs/home.html",{"category":mydata})
        else:
            return render(request,"myblogs/home.html",{"warning":'No record found'})



def Contact(request):
    # return HttpResponse('<h1>This is My Contact Page </h1>')
   if request.method == 'GET':
        return render(request, 'myblogs/contact.html')
   elif request.method == 'POST':
        email = request.POST.get('user_email')
        message = request.POST.get('message')
        x = contact_info(u_email=email, u_message=message)
        x.save()
        print(email)
        print(message)

        return render(request,"myblogs/contact.html",{'feedback':'Your message has been recorded'})

@login_required(login_url="loginuser")
def newsletter(request):
#    return HttpResponse('<h1> Sucbcribe to Our Newsletter </h1>')
   if request.method == 'GET':
        return render(request, 'myblogs/newsletter.html')
   elif request.method == 'POST':
        email = request.POST.get('email')
        y = subscription(email=email)
        if(subscription.objects.filter(email = email).exists()):
          return render(request,"myblogs/newsletter.html",{'feedback':'You are already subscribed'})   
        else:
          y.save()
          print(email)
          return render(request,"myblogs/newsletter.html",{'feedback':'You are subscribed now'}) 
          
            
       

def Support(request):
    # return HttpResponse('<h1>This is My Support Page </h1>')
    return render(request,"myblogs/support.html")


# @login_required(login_url="loginuser")
def blog_cat(request):
    x = Blog_Form()  
    if request.method == "GET":
        return render(request,'myblogs/blog_cat.html',{"x":x})
    else:
        print("hi")
        form = Blog_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("hi")
            return redirect('home')
        else:
            return render(request,'myblogs/blog_cat.html',{"x":x})

def ck(request):
    x = BlogPost_Form()
    return render(request,'myblogs/ck.html',{"x":x}) 

@login_required(login_url="loginuser")
def blog(request):
    x = BlogPost_Form()  
    if request.method == "GET":
        return render(request,'myblogs/blog.html',{"x":x})
    else:
        print("hi")
        form = BlogPost_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("hi")
            return redirect('home')
        else:
            return render(request,'myblogs/blog.html',{"x":x})   

# @login_required(login_url="loginuser")
def allblogs(request):
    y=blog_post.objects.all()
    paginator = Paginator(y, 3)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'myblogs/allblogs.html',{"y":page_obj})
    # return render(request,'myblogs/allblogs.html',{"y":y})            


def blog_details(request, blog_id):
    y=blog_post.objects.get(id=blog_id)
    return render(request,'myblogs/blog_details.html',{"y":y}) 
    # z=obj.view_count
    # z=z+1
    # obj.view_count=z
    # obj.save() 

def loginuser(request):
    if request.method =='GET':
        return render(request, 'myblogs/loginuser.html', {'form':AuthenticationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password')
        user = authenticate(request, username=a, password=b)
        if user is None:
            return render(request, 'myblogs/loginuser.html', {'form':AuthenticationForm(), 'error':'Invalid Cerdentials'})
        else:
            login(request, user)
            return redirect('home')

def signupuser(request):
    if request.method =='POST':
        return render(request, 'myblogs/signupuser.html', {'form':UserCreationForm()})    
    else:
        a = request.POST.get('username')
        b = request.POST.get('password1')
        c = request.POST.get('password2')
        if b==c:
            if (User.objects.filter(username =a)):
                return render(request, 'myblogs/signupuser.html', {'form':UserCreationForm(),'error': 'Password Mismatch Try Again'})
            else:
                user = User.objects.create_user(username = a, password=b)
                user.save()
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'myblogs/signupuser.html', {'form':UserCreationForm(),'error': 'Password Mismatch Try Again'})

def logoutuser(request):
    if request.method =='GET':
        logout(request)
        return redirect('home')
    
    # Blog_category to all blog category wise
def cat(request, cat_id):
    x = Blog_Category.objects.get(blog_cat = cat_id)
    blogs = blog_post.objects.filter(blog_cat=x)
    return render(request,'myblogs/allblogs.html',{"y":blogs})    

def add_like(request, blog_id):
    obj = get_object_or_404(blog_post, pk=blog_id)
    print (obj.like_count)
    y=obj.like_count
    y=y+1
    obj.like_count=y
    obj.save()
    return redirect('blog_details', obj.id)