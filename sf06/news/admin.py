from django.contrib import admin
from .models import Author, Post, Comment, Category, PostCategory

class PostCategories(admin.TabularInline):
    model = PostCategory
    extra = 2

class PostAdmin(admin.ModelAdmin):
    inlines = (PostCategories,)


admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)

# Register your models here.