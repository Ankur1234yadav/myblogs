from django.contrib import admin
from .models import Blog_Category, contact_info, subscription, blog_post
# Register your models here.
admin.site.register(Blog_Category)
admin.site.register(contact_info)
admin.site.register(subscription)
admin.site.register(blog_post)

