from django.contrib import admin
from .models import ThemeConfig
from .forms import ThemeConfigForm


@admin.register(ThemeConfig)
class ThemeConfigAdmin(admin.ModelAdmin):
    form = ThemeConfigForm
    fieldsets = (
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
    list_display = ['id']
