from django.contrib import admin

from root.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class CriterionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category', )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'provider')
    list_filter = ('category', )


class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    list_filter = ('product',)


class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('product', 'criterion', 'value')
    list_filter = ('product', 'criterion')


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'description')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('owner', 'product', 'mark')
    list_filter = ('product', 'owner')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date', 'status', 'total_cost')
    list_filter = ('status', 'customer')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date', 'title')
    list_filter = ('owner', 'date')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email', 'address')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'likes_count',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Criterion, CriterionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Like, LikeAdmin)


