from django.contrib import admin
from .models import Blog, Category, BlogStats

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','status', 'created_at', 'updated_at', 'image')

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)

class StatsAdmin(admin.ModelAdmin):
    list_display = ('blog', 'blog_clicks','unique_views', 'created_at', 'updated_at')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
admin.site.register(BlogStats, StatsAdmin)
