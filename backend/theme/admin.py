from django.contrib import admin
from .models import ThemeConfig

# Register your models here.
@admin.register(ThemeConfig)
class ThemeConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'active')
        }),
        ('URLs', {
            'fields': ('font_url', 'logo_url', 'background_url')
        }),
    )
    readonly_fields = ('active',)
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(active=True)

    make_active.short_description = "Make selected themes active"

    def make_inactive(self, request, queryset):
        queryset.update(active=False)

    make_inactive.short_description = "Make selected themes inactive"
    