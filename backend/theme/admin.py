import re
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import ThemeConfig
from .forms import ThemeConfigForm


@admin.register(ThemeConfig)
class ThemeConfigAdmin(admin.ModelAdmin):

    form = ThemeConfigForm

    fieldsets = (
        ('Theme Configuration', {
            'fields': ('name',)
        }),
        ('Status', {
            'fields': ('active',)
        }),
        ('Font Configuration', {
            'description': 'Please use a valid font-family name, url or enter the name or url of a font from Google Fonts (e.g. Roboto, Fredoka, Open Sans). See also <a href="https://fonts.google.com/" target="_blank">Google Fonts</a>',
            'fields': ('font',)
        }),
        ('Logo Configuration', {
            'fields': ('logo',)
        }),
        ('Background Configuration', {
            'fields': ('background',)
        }),
        ('Color Configuration', {
            'fields': ('teal', 'yellow', 'pink', 'red', 'blue', 'green', 'indigo', 'gray', 'gray_900', 'black')
        }),
        ('Design Tokens', {
            'fields': ('primary', 'success', 'positive', 'negative',
                       'secondary', 'info')
        }),
        ('Additional Variables', {
            'description': 'Please use the following format: <code>--variable-name: value;</code>\
                            <br>For example: <code>--aqua: #00ffff;</code>',
            'fields': ('additional_variables',)
        }),
        ('Global Custom CSS', {
            'description': 'Please use the following format: <code>selector { property: value; }</code>\
                            <br>For example: <code>body { background-color: var(--aqua); }</code>',
            'fields': ('global_css',)
        }),
    )

    list_display = ('id', 'name_link', 'font_preview', 'logo_preview', 'background_preview', 'active')

    def name_link(self, obj):
        return format_html('<a href="{}">{}</a>', f'/admin/theme/themeconfig/{obj.id}/change/', obj.name)

    def font_preview(self, obj):
        if obj.font:
            # Check if the font field contains a URL
            if obj.font.startswith('http://') or obj.font.startswith('https://'):
                # Extract font-family name from URL
                font_family_match = re.search(r'family=([^&:]+)', obj.font)
                font_family = font_family_match.group(1).replace("+", " ") if font_family_match else "sans-serif"

                return format_html(
                    '<link href="{font_url}" rel="stylesheet">'
                    '<div style="font-family: \'{font_family}\'; font-size: 16px;">Preview Text</div>',
                    font_url=obj.font,
                    font_family=font_family
                )
            else:
                # Font is specified as a Google Font name
                font_name = obj.font.replace(" ", "+")  # Replace spaces with '+' for the URL
                return format_html(
                    '<link href="https://fonts.googleapis.com/css2?family={font_name}&display=swap" rel="stylesheet">'
                    '<div style="font-family: \'{font}\'; font-size: 16px;">Preview Text</div>',
                    font_name=font_name,
                    font=obj.font
                )
        return "No font selected"

    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo}" style="max-height: 50px;"/>')
        return ""

    def background_preview(self, obj):
        if obj.background:
            return mark_safe(f'<div style="background-image: url({obj.background}); height: 50px; width: 100px; background-size: cover;"></div>')
        return ""

    font_preview.short_description = 'Font Preview'
    logo_preview.short_description = 'Logo Preview'
    background_preview.short_description = 'Background Preview'
    font_preview.allow_tags = True
    logo_preview.allow_tags = True
    background_preview.allow_tags = True