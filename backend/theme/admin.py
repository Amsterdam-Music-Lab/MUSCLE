import re

from django.conf import settings
from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from django.utils.html import format_html
from .models import FooterConfig, HeaderConfig, ThemeConfig, SponsorImage
from .forms import ThemeConfigForm


class SponsorImageInline(NestedTabularInline):
    model = SponsorImage
    extra = 1
    sortable_field_name = "index"
    ordering = ["index"]


class FooterConfigInline(NestedStackedInline):
    model = FooterConfig
    inlines = [SponsorImageInline]


class HeaderConfigInline(NestedStackedInline):
    model = HeaderConfig
    fields = ["show_score"]


@admin.register(ThemeConfig)
class ThemeConfigAdmin(NestedModelAdmin):  # Change this line
    form = ThemeConfigForm
    inlines = [HeaderConfigInline, FooterConfigInline]

    list_display = (
        "name",
        "header_overview",
        "heading_font_preview",
        "body_font_preview",
        "logo_preview",
        "background_preview",
        "footer_overview",
    )
    search_fields = ("name", "description")
    ordering = ("name",)
    fieldsets = (
        (None, {"fields": ("name", "description")}),
        (
            "Colors Configuration",
            {
                "fields": (
                    "color_primary",
                    "color_secondary",
                    "color_positive",
                    "color_negative",
                    "color_neutral1",
                    "color_neutral2",
                    "color_neutral3",
                    "color_text",
                    "color_background",
                    "color_grey",
                )
            },
        ),
        (
            "Heading Font Configuration",
            {
                "description": 'Please use a valid font-family name, url or enter the name or url of a font from Google Fonts (e.g. Roboto, Fredoka, Open Sans). See also <a href="https://fonts.google.com/" target="_blank">Google Fonts</a>',
                "fields": ("heading_font_url",),
            },
        ),
        (
            "Body Font Configuration",
            {
                "description": 'Please use a valid font-family name, url or enter the name or url of a font from Google Fonts (e.g. Roboto, Fredoka, Open Sans). See also <a href="https://fonts.google.com/" target="_blank">Google Fonts</a>',
                "fields": ("body_font_url",),
            },
        ),
        ("Logo Configuration", {"fields": ("logo_image",)}),
        ("Background Configuration", {"fields": ("background_image",)}),
    )

    def header_overview(self, obj):
        return "Header set" if obj.header else ""

    def footer_overview(self, obj):
        return f"Footer with {obj.footer.sponsor_images.count()} logos"

    def heading_font_preview(self, obj):
        if obj.heading_font_url:
            # Check if the font field contains a URL
            if obj.heading_font_url.startswith(
                "http://"
            ) or obj.heading_font_url.startswith("https://"):
                # Extract font-family name from URL
                font_family_match = re.search(r"family=([^&:]+)", obj.heading_font_url)
                font_family = (
                    font_family_match.group(1).replace("+", " ")
                    if font_family_match
                    else "sans-serif"
                )

                return format_html(
                    '<link href="{heading_font_url}" rel="stylesheet">'
                    "<div style=\"font-family: '{font_family}'; font-size: 16px;\">Preview Text</div>",
                    heading_font_url=obj.heading_font_url,
                    font_family=font_family,
                )
            else:
                # Font is specified as a Google Font name
                font_name = obj.heading_font_url.replace(
                    " ", "+"
                )  # Replace spaces with '+' for the URL
                return format_html(
                    '<link href="https://fonts.googleapis.com/css2?family={font_name}&display=swap" rel="stylesheet">'
                    "<div style=\"font-family: '{font}'; font-size: 16px;\">Preview Text</div>",
                    font_name=font_name,
                    font=obj.heading_font_url,
                )
        return "No font selected"

    def body_font_preview(self, obj):
        if obj.body_font_url:
            # Check if the font field contains a URL
            if obj.body_font_url.startswith("http://") or obj.body_font_url.startswith(
                "https://"
            ):
                # Extract font-family name from URL
                font_family_match = re.search(r"family=([^&:]+)", obj.body_font_url)
                font_family = (
                    font_family_match.group(1).replace("+", " ")
                    if font_family_match
                    else "sans-serif"
                )

                return format_html(
                    '<link href="{body_font_url}" rel="stylesheet">'
                    "<div style=\"font-family: '{font_family}'; font-size: 16px;\">Preview Text</div>",
                    body_font_url=obj.body_font_url,
                    font_family=font_family,
                )
            else:
                # Font is specified as a Google Font name
                font_name = obj.body_font_url.replace(" ", "+")
                return format_html(
                    '<link href="https://fonts.googleapis.com/css2?family={font_name}&display=swap" rel="stylesheet">'
                    "<div style=\"font-family: '{font}'; font-size: 16px;\">Preview Text</div>",
                    font_name=font_name,
                    font=obj.body_font_url,
                )
        return "No font selected"

    def logo_preview(self, obj):
        if obj.logo_image:
            return format_html(
                f'<img src="{settings.MEDIA_URL}{obj.logo_image.file}" style="max-height: 50px;"/>'
            )
        return ""

    def background_preview(self, obj):
        if obj.background_image:
            return format_html(
                f'<div style="background-image: url({settings.MEDIA_URL}{obj.background_image.file}); height: 50px; width: 100px; background-size: cover;"></div>'
            )
        return ""

    heading_font_preview.short_description = "Heading Font Preview"
    body_font_preview.short_description = "Body Font Preview"
    logo_preview.short_description = "Logo Preview"
    background_preview.short_description = "Background Preview"
    heading_font_preview.allow_tags = True
    body_font_preview.allow_tags = True
    logo_preview.allow_tags = True
    background_preview.allow_tags = True
