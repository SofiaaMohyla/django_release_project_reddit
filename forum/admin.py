from django.contrib import admin

from .models import Post, Commentary, Branch, Rating, Grade

# Register your models here.

class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'description', )
    list_display_links = ('name', 'description', )

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'branch', 'author', 'description', )
    list_display_links = ('title', 'description', )

class CommentaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'text', )
    list_display_links = ('text', )


admin.site.register(Post, PostAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Commentary, CommentaryAdmin)
admin.site.register(Rating)
admin.site.register(Grade)