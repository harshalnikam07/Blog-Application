from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User        #imported by me, for authentication
from django.contrib.auth import authenticate         #imported by me, for authentication
from django.contrib.auth import login,logout
from myapp.models import Post,SubPlan,Author      
from django.db.models import Q          #Q class
import razorpay
from django.core.mail import send_mail      #imported for email integration

# Create your views here.
def register(request):
    context={}
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        uname=request.POST['uname']
        ue=request.POST['uemail']
        p=request.POST['upass']
        cp=request.POST['ucpass']

        if uname=='' or ue=='' or p=='' or cp=='':
            # print('Please fill all the fields')
            context['errormsg']='Please fill all the fields'
        elif len(p)<8:
            # print('Password must be atleast 8 character')
            context['errormsg']='Password must be atleast 8 character'
        elif p!=cp:
            # print('Password and Confirm password must be same')
            context['errormsg']='Password and Confirm password must be same'
        else:
            try:
                u=User.objects.create(username=ue,email=ue,first_name=uname)
                u.set_password(p)  #set_password : it is used to convert password into encripted password
                u.save()
                context['success']='User Created Successfully'
            except Exception:
                context['errormsg']='User Already Exists'
        return render(request,'register.html',context)
    



def user_login(request):
    context={}
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        e=request.POST['ue']
        p=request.POST['upass']
        u=authenticate(username=e,password=p) #also import from auth
        if u is not None:
            login(request,u)        #also import from auth
            return redirect('/home')
        else:
            context['errormsg']='Invalid Credential'
            return render(request,'login.html',context)
        
# Forgot Password function
from django.contrib import messages

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset_link = f"http://yourdomain.com/reset-password/{user.id}"  # Create reset link
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'nikamharshal117@gmail.com',
                [email],
                fail_silently=False,
            )
            # Using messages.success() to display success message
            messages.success(request, 'Password reset link has been sent to your email.')
        except User.DoesNotExist:
            # Using messages.error() to display error message
            messages.error(request, 'No user found with this email address.')
    
    return render(request, 'forgot_password.html')

        

# home page of BlogApp
def home(request):
    # u=Post.objects.filter(author=request.user.id)
    u=Post.objects.all()
    context={}
    context['data']=u
    return render(request, 'home.html', context)


def user_logout(request):
    logout(request)
    return redirect('/home')


# to post blog 
def postblog(request):
    context={}
    if request.user.is_authenticated :
        if request.method == 'GET':
            return render(request, 'postblog.html')
        else:
            t=request.POST['title']
            cat=request.POST['category']
            con=request.POST['content']
            img=request.POST['image']
            aid=request.user
            # print(t)
            # print(cat)
            # print(con)
            # print(img)
            # print(aid)
            if t=='' or cat=='' or con=='' or img=='':
                # print('Please fill all the fields')
                context['errormsg']='Please fill all the fields'
            elif len(con)>2000:
                # print('Password must be atleast 8 character')
                context['errormsg']='Content should be less than 2000 characters'
            else:
                try:
                    u=Post.objects.create(title=t,category=cat,content=con,image=img,author=aid)
                    u.save()
                    context['success']='Blog Posted Successfully'  
                except Exception:
                    context['errormsg']='Error occured, try again..!'             
        return render(request,'postblog.html',context)
    else:
        return redirect('/login')


# myblog : posted by authenticated user 
def myblogs(request):
    context={}
    u=Post.objects.filter(author=request.user.id)
    # print(u)
    context['data']=u
    # HttpResponse('fetched')
    return render(request, 'myblogs.html', context)
    
    

def exploreblog(request):
    p=Post.objects.order_by('-created_at')      #display blog on desc order of post date
    context={}
    context['data']=p
    return render(request, 'exploreblog.html', context)





# Filter by author name 
def search(request):
    context={}
    s=request.GET['srch']
    print(s)

    a=Post.objects.filter(author__first_name__icontains=s)
    print(a)
    context['data']=a
    return render(request, 'home.html', context)




# Filter by category name : status incomplete
# def filterCat(request, cat):
#     context={}
#     f=Post.objects.filter(category=cat)

#     context['data']=f
#     return render(request, 'home.html', context)







# Edit particular post posted by authenticated user
def edit(request,bid):
    context={}
    b=Post.objects.filter(id=bid)
    if request.method == 'GET':
        context['data']=b
        return render(request, 'editpost.html', context)
    else:
        t=request.POST['title']
        cat=request.POST['category']
        con=request.POST['content']
        img=request.POST['image']
        if t=='' or cat=='' or con=='' or img=='':
            context['errormsg']='Please fill all the fields'
        elif len(con)>2000:
            context['errormsg']='Content should be less than 2000 characters'
        else:
            try:
                b.update(title=t,category=cat,content=con,image=img )
                context['success']='Blog has been updated..!'
            except Exception:
                context['errormsg']='Error occured, try again..!'
    return render(request, 'editpost.html', context)




#  Delete particular post posted by authenticated user
def delete(request,bid):
    context={}
    b=Post.objects.filter(id=bid)
    # print(b)
    b.delete()
    # b.save()
    context['success']='Blog has been Deleted...!'
    return render(request,'myblogs.html', context)
    


# aboutus page 
def aboutus(request):
    return render(request,'aboutus.html')


# subscription page 
def subscribe(request):
    context={}
    b=SubPlan.objects.all()
    if request.user.is_authenticated :
        context['data']=b
        return render(request, 'subscribe.html', context)
    else:
        return redirect('/login')



# pay.html : 
def pay(request,pid):
    context={}
    client = razorpay.Client(auth=("rzp_test_c66P03WlENQIxJ", "Om1tOy0A2HuYZUT0rHFnZgTd"))

    r=SubPlan.objects.filter(id=pid)   #calculate the total amount to pay and add amt to dict
    # print(r)
    amt=r[0].price

    amt=amt*100 # to convert amount to paise 
    # print(amt)
    data = { "amount": amt, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    context['payment']=payment

    a=User.objects.filter(id=request.user.id)
    # print(a)
    p=SubPlan.objects.filter(id=pid)
    # q1=Q(aid=a[0])
    # q2=Q(sub_plan=p[0])
    # c=Author.objects.filter(q1 & q2)
    
    c=Author.objects.create(aid=a[0],sub_plan=p[0])         
    c.save()
    return render(request,'pay.html')





#paymentsuccess page after placing order
def paymentsuccess(request):
    sub='Blog-Crafters Subscription Status'
    msg="Thank you for being a part of Blog-Crafters! Your subscription is currently active, giving you access to exclusive content and updates. Keep crafting your story!"
    frm='nikamharshal@gmail.com'

    u=User.objects.filter(id=request.user.id)       #email should go to authenticated user only 
    to=u[0].email

    send_mail(
        sub,
        msg,
        frm,
        [to],               #list beacause we can send mail to multiple emails-ids
        fail_silently=False
    )
    return render(request, 'paymentsuccess.html')
        

def myprofile(request):
    context={}
    a=Author.objects.filter(aid=request.user.id)
    print(a)
    context['data']=a
    return render(request, 'myprofile.html', context)

def post_detail(request, post_id):
    # Specific blog post fetch by ID
    context={}
    print(post_id)
    post = Post.objects.filter(id=post_id)
    print(post)
    context['post']=post
    return render(request, 'blog_post_detail.html',context)
























