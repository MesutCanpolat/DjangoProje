from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from images.models import Category, Images, Foto, Comment


class ImagesImageInline(admin.TabularInline):
    model = Foto
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status']


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'status', 'description']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category', 'title', 'description']
    inlines = [ImagesImageInline]
    prepopulated_fields = {'slug': ('title',)}

class FotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'images', 'image_tag']
    readonly_fields = ('image_tag',)


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug':('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Images,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Images,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Related products (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'image', 'user', 'status']
    list_filter = ['status']



admin.site.register(Category, CategoryAdmin2)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Foto, FotoAdmin)
admin.site.register(Comment, CommentAdmin)

