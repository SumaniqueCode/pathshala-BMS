from django.contrib import admin
from .models import Blog, Category

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'image')

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
