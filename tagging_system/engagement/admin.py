from django.contrib import admin
from .models import Post, PostImage, UserPostTagWeightage


class PostModelAdmin(admin.ModelAdmin):
    list_display = ("description", "tag", "created_by", "created_at", "updated_at")


admin.site.register(Post, PostModelAdmin)


class PostImageModelAdmin(admin.ModelAdmin):
    list_display = ("post", "image")


admin.site.register(PostImage, PostImageModelAdmin)


class UserPostTagWeightageAdmin(admin.ModelAdmin):
    list_display = ("user", "tag", "weightage")


admin.site.register(UserPostTagWeightage, UserPostTagWeightageAdmin)