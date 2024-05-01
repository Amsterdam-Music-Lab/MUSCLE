from django.contrib import admin
from .models import AdminInterfaceConfiguration, AdminInterfaceThemeConfiguration


class AdminInterfaceThemeConfigurationInline(admin.StackedInline):
    model = AdminInterfaceThemeConfiguration
    extra = 0
    fields = (
        # Color scheme
        
        ## Official Django colors

        ### Main colors
        'color_primary',
        'color_secondary',
        'color_accent',
        'color_primary_fg',

        ### Body
        'color_body_fg',
        'color_body_bg',
        'color_body_quiet_color',
        'color_body_loud_color',

        ### Header
        'color_header_color',

        ### Breadcumbs
        'color_breadcrumbs_fg',

        ### Link
        'color_link_fg',
        'color_link_hover_color',
        'color_link_selected_fg',

        ### Borders
        'color_hairline_color',
        'color_border_color',

        ### Error
        'color_error_fg',

        ### Message
        'color_message_success_bg',
        'color_message_warning_bg',
        'color_message_error_bg',

        ### Darkened
        'color_darkened_bg',

        ### Selected
        'color_selected_bg',
        'color_selected_row',

        ### Button
        'color_button_fg',
        'color_button_bg',
        'color_button_hover_bg',
        'color_default_button_bg',
        'color_default_button_hover_bg',
        'color_close_button_bg',
        'color_close_button_hover_bg',
        'color_delete_button_bg',
        'color_delete_button_hover_bg',

        # Custom colors
        'color_default_bg',
        'color_default_fg',
        'color_success_bg',
        'color_success_fg',
        'color_warning_bg',
        'color_warning_fg',
        'color_error_bg',
    )


class AdminInterfaceConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

    inlines = [AdminInterfaceThemeConfigurationInline]


admin.site.register(
    AdminInterfaceConfiguration,
    AdminInterfaceConfigurationAdmin,
)
