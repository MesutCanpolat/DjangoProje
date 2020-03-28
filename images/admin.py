from django.contrib import admin

# Register your models here.
from images.models import Category, Images, Foto


class ImagesImageInline(admin.TabularInline):
    model = Foto
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status']


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'status', 'description']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category', 'title', 'description']
    inlines = [ImagesImageInline]


class FotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'images', 'image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Foto, FotoAdmin)
