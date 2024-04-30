from django.contrib import admin
from .models import AdminInterfaceConfiguration, AdminInterfaceThemeConfiguration


class AdminInterfaceThemeConfigurationInline(admin.StackedInline):
    model = AdminInterfaceThemeConfiguration
    extra = 0
    fields = ('color_default_bg', 'color_default_fg', 'color_success_bg', 'color_success_fg', 'color_warning_bg', 'color_warning_fg', 'color_error_bg', 'color_error_fg')


class AdminInterfaceConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

    inlines = [AdminInterfaceThemeConfigurationInline]


admin.site.register(AdminInterfaceConfiguration, AdminInterfaceConfigurationAdmin)
admin.site.register(AdminInterfaceThemeConfiguration)
