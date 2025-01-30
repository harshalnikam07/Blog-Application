from django.contrib import admin
from myapp.models import Post,Author,SubPlan     #imported 

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=['id','title','category','content','author','created_at','updated_at','image']
    list_filter=['category']

class AuthorAdmin(admin.ModelAdmin):
    list_display=['id','aid','sub_plan']
    list_filter=['sub_plan']

class SubPlanAdmin(admin.ModelAdmin):
    list_display=['id','sub_plan','price','no_of_post']
    list_filter=['sub_plan']

admin.site.register(Post,PostAdmin) 
admin.site.register(Author,AuthorAdmin) 
admin.site.register(SubPlan,SubPlanAdmin) 