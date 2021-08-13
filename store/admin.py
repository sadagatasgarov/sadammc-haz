from django.contrib import admin

from store.models import Product, ProductGalery, Variation, ReviewRating
import admin_thumbnails
# Register your models here.



@admin_thumbnails.thumbnail('image')
class ProductGaleryInline(admin.TabularInline):
    model = ProductGalery
    extra =1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGaleryInline]
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active','created_date')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value','is_active','created_date')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGalery)
