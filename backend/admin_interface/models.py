from django.db import models


class AdminInterfaceConfiguration(models.Model):
    """Model for storing the configuration of the admin interface"""
    name = models.CharField(max_length=255, unique=True, default='Default')
    description = models.TextField(blank=True, default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'name': self.name,
            'description': self.description,
        }


class AdminInterfaceThemeConfiguration(models.Model):
    """Model for storing the theme configuration of the admin interface"""
    configuration = models.OneToOneField(
        AdminInterfaceConfiguration, on_delete=models.CASCADE, related_name='theme')

    # Color scheme

    ## Official Django colors

    ### Main colors
    color_primary = models.CharField(max_length=255, blank=True, default='#79aec8')
    color_secondary = models.CharField(max_length=255, blank=True, default='#417690')
    color_accent = models.CharField(max_length=255, blank=True, default='#f5dd5d')
    color_primary_fg = models.CharField(max_length=255, blank=True, default='#fff')

    ### Body
    color_body_fg = models.CharField(max_length=255, blank=True, default='#333')
    color_body_bg = models.CharField(max_length=255, blank=True, default='#fff')
    color_body_quiet_color = models.CharField(max_length=255, blank=True, default='#666')
    color_body_loud_color = models.CharField(max_length=255, blank=True, default='#000')

    ### Header
    color_header_color = models.CharField(max_length=255, blank=True, default='#ffc')

    ### Breadcumbs
    color_breadcrumbs_fg = models.CharField(max_length=255, blank=True, default='#c4dce8')

    ### Link
    color_link_fg = models.CharField(max_length=255, blank=True, default='#447e9b')
    color_link_hover_color = models.CharField(max_length=255, blank=True, default='#036')
    color_link_selected_fg = models.CharField(max_length=255, blank=True, default='#5b80b2')

    ### Borders
    color_hairline_color = models.CharField(max_length=255, blank=True, default='#e8e8e8')
    color_border_color = models.CharField(max_length=255, blank=True, default='#ccc')

    ### Error
    color_error_fg = models.CharField(max_length=255, blank=True, default='#ba2121')

    ### Message
    color_message_success_bg = models.CharField(max_length=255, blank=True, default='#dfd')
    color_message_warning_bg = models.CharField(max_length=255, blank=True, default='#ffc')
    color_message_error_bg = models.CharField(max_length=255, blank=True, default='#ffefef')

    ### Darkened
    color_darkened_bg = models.CharField(max_length=255, blank=True, default='#f8f8f8')

    ### Selected
    color_selected_bg = models.CharField(max_length=255, blank=True, default='#e4e4e4')
    color_selected_row = models.CharField(max_length=255, blank=True, default='#ffc')

    ### Button
    color_button_fg = models.CharField(max_length=255, blank=True, default='#fff')
    color_button_bg = models.CharField(max_length=255, blank=True, default='#79aec8')
    color_button_hover_bg = models.CharField(max_length=255, blank=True, default='#609ab6')
    color_default_button_bg = models.CharField(max_length=255, blank=True, default='#417690')
    color_default_button_hover_bg = models.CharField(max_length=255, blank=True, default='#205067')
    color_close_button_bg = models.CharField(max_length=255, blank=True, default='#888')
    color_close_button_hover_bg = models.CharField(max_length=255, blank=True, default='#747474')
    color_delete_button_bg = models.CharField(max_length=255, blank=True, default='#ba2121')
    color_delete_button_hover_bg = models.CharField(max_length=255, blank=True, default='#a41515')

    ## Custom colors
    color_default_bg = models.CharField(max_length=255, blank=True, default='#f8d7da')
    color_default_fg = models.CharField(max_length=255, blank=True, default='#721c24')
    color_success_bg = models.CharField(max_length=255, blank=True, default='#d4edda')
    color_success_fg = models.CharField(max_length=255, blank=True, default='#155724')
    color_warning_bg = models.CharField(max_length=255, blank=True, default='#fff3cd')
    color_warning_fg = models.CharField(max_length=255, blank=True, default='#856404')
    color_error_bg = models.CharField(max_length=255, blank=True, default='#f8d7da')
