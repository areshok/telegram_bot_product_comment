from django.contrib import admin

# Register your models here.

from .models import Marketplace, Product, ProductMarketplace, Score ,CommentProduct


admin.site.register(Marketplace)
admin.site.register(Product)
admin.site.register(ProductMarketplace)
admin.site.register(Score)
admin.site.register(CommentProduct)



