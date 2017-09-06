from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Criterion)
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Characteristic)
admin.site.register(Provider)
admin.site.register(Feedback)
admin.site.register(Order)
admin.site.register(Message)

