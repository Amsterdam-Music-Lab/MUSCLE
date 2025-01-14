from django import template

register = template.Library()


@register.filter(name="get_langcode")
def get_langcode(formset):
    langcodes = []
    for obj in formset.formset.queryset:
        langcodes.append(obj.language)
    return langcodes


@register.filter(name="get_block_slug")
def get_block_slug(formset):
    return formset.instance.slug
