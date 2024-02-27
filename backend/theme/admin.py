import re
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import ThemeConfig
from .forms import ThemeConfigForm


@admin.register(ThemeConfig)
class ThemeConfigAdmin(admin.ModelAdmin):

    form = ThemeConfigForm

    list_display = ('id', 'name_link', 'font_preview', 'logo_preview', 'background_preview', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'active')
        }),
        ('Font Configuration', {
            'description': 'Please use a valid font-family name, url or enter the name or url of a font from Google Fonts (e.g. Roboto, Fredoka, Open Sans). See also <a href="https://fonts.google.com/" target="_blank">Google Fonts</a>',
            'fields': ('font_url',)
        }),
        ('Logo Configuration', {
            'fields': ('logo_url',)
        }),
        ('Background Configuration', {
            'fields': ('background_url',)
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

    def name_link(self, obj):
        return format_html('<a href="{}">{}</a>', f'/admin/theme/themeconfig/{obj.id}/change/', obj.name)

    def font_preview(self, obj):
        if obj.font_url:
            # Check if the font field contains a URL
            if obj.font_url.startswith('http://') or obj.font_url.startswith('https://'):
                # Extract font-family name from URL
                font_family_match = re.search(r'family=([^&:]+)', obj.font_url)
                font_family = font_family_match.group(1).replace("+", " ") if font_family_match else "sans-serif"

                return format_html(
                    '<link href="{font_url}" rel="stylesheet">'
                    '<div style="font-family: \'{font_family}\'; font-size: 16px;">Preview Text</div>',
                    font_url=obj.font_url,
                    font_family=font_family
                )
            else:
                # Font is specified as a Google Font name
                font_name = obj.font_url.replace(" ", "+")  # Replace spaces with '+' for the URL
                return format_html(
                    '<link href="https://fonts.googleapis.com/css2?family={font_name}&display=swap" rel="stylesheet">'
                    '<div style="font-family: \'{font}\'; font-size: 16px;">Preview Text</div>',
                    font_name=font_name,
                    font=obj.font_url
                )
        return "No font selected"

    def logo_preview(self, obj):
        if obj.logo_url:
            return mark_safe(f'<img src="{obj.logo_url}" style="max-height: 50px;"/>')
        return ""

    def background_preview(self, obj):
        if obj.background_url:
            return mark_safe(f'<div style="background-image: url({obj.background_url}); height: 50px; width: 100px; background-size: cover;"></div>')
        return ""

    font_preview.short_description = 'Font Preview'
    logo_preview.short_description = 'Logo Preview'
    background_preview.short_description = 'Background Preview'
    font_preview.allow_tags = True
    logo_preview.allow_tags = True
    background_preview.allow_tags = True
