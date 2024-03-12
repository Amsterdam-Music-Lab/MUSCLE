from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Image
from .forms import ImageAdminForm


class TagsListFilter(admin.SimpleListFilter):
    title = 'tags'
    parameter_name = 'tags'

    def lookups(self, request, model_admin):
        tags = Image.objects.values_list('tags', flat=True)
        unique_tags = set(tag for sublist in tags for tag in sublist)
        return [(tag, tag) for tag in unique_tags]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags__contains=[self.value()])
        return queryset


class ImageAdmin(admin.ModelAdmin):

    form = ImageAdminForm

    list_display = ('image_preview', 'title', 'description', 'tags', 'created_at')
    search_fields = ['title', 'description', 'tags']
    list_filter = [TagsListFilter]
    fields = ['file', 'title', 'description', 'alt', 'href', 'rel',
              'target', 'tags']
    readonly_fields = ['created_at', 'updated_at']

    def image_preview(self, obj):
        if obj.file and obj.file.url:
            return mark_safe(f'<img src="{obj.file.url}" style="max-height: 50px;"/>')
        return ""

    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'


admin.site.register(Image, ImageAdmin)
