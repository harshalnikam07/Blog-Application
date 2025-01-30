from django.urls import include, path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login', views.user_login),
    path('register', views.register),
    path('logout',views.user_logout),
    path('home', views.home),
    path('postblog', views.postblog),
    path('myblogs', views.myblogs),
    path('exploreblog', views.exploreblog),
    path('search', views.search),    #search by author name
    # path('filterCat', views.filterCat),    #search by category
    path('edit/<bid>', views.edit),    
    path('delete/<bid>', views.delete),    
    path('subscribe', views.subscribe),    
    path('aboutus', views.aboutus),    
    path('pay/<pid>', views.pay),    
    path('paymentsuccess', views.paymentsuccess),   
    path('myprofile', views.myprofile),
    path('post/<post_id>', views.post_detail), 
    path('forgot-password/', views.forgot_password),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)