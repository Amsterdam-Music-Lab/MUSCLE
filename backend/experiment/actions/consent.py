from os.path import splitext

from django.template.loader import render_to_string
from django.template import Template, Context
from django_markup.markup import formatter
from django.core.files import File

from .base_action import BaseAction


def get_render_format(url: str) -> str:
    """
    Detect markdown file based on file extension

    Args:
        url: Url of the consent file

    Returns:
        File format

    """
    if splitext(url)[1] == ".md":
        return "MARKDOWN"
    return "HTML"


def render_html_or_markdown(dry_text: str, render_format: str) -> str:
    """render html or markdown

    Args:
        dry_text: contents of a markdown or html file
        render_format: type of contents, either 'HTML' or 'MARKDOWN'

    Returns:
        Content rendered to html
    """

    if render_format == "HTML":
        template = Template(dry_text)
        context = Context()
        return template.render(context)
    if render_format == "MARKDOWN":
        return formatter(dry_text, filter_name="markdown")


class Consent(BaseAction):  # pylint: disable=too-few-public-methods
    """Provide data for a view that ask consent for using the experiment data

    Args:
        text: Uploaded file via an experiment's translated content's consent (fileField)
        title: The title to be displayed
        confirm: The text on the confirm button
        deny: The text on the deny button
        url:  If no text is provided the url will be used to load a template (HTML or MARKDOWN)
                    HTML: (default) Allowed tags: html, django template language
                    MARKDOWN: Allowed tags: Markdown language

    Note:
        Relates to client component: Consent.tsx
    """

    # default consent text, that can be used for multiple blocks
    ID = "CONSENT"

    default_text = "Lorem ipsum dolor sit amet, nec te atqui scribentur. Diam \
                molestie posidonium te sit, ea sea expetenda suscipiantur \
                contentiones, vix ex maiorum denique! Lorem ipsum dolor sit \
                amet, nec te atqui scribentur. Diam molestie posidonium te sit, \
                ea sea expetenda suscipiantur contentiones, vix ex maiorum \
                denique! Lorem ipsum dolor sit amet, nec te atqui scribentur. \
                Diam molestie posidonium te sit, ea sea expetenda suscipiantur \
                contentiones, vix ex maiorum denique! Lorem ipsum dolor sit \
                amet, nec te atqui scribentur. Diam molestie posidonium te sit, \
                ea sea expetenda suscipiantur contentiones."

    def __init__(
        self, text: File, title: str = "Informed consent", confirm: str = "I agree", deny: str = "Stop", url: str = ""
    ) -> dict:
        # Determine which text to use
        if text != "":
            # Uploaded consent via file field: block.consent (High priority)
            with text.open("r") as f:
                dry_text = f.read()
            render_format = get_render_format(text.url)
        elif url != "":
            # Template file via url (Low priority)
            dry_text = render_to_string(url)
            render_format = get_render_format(url)
        else:
            # use default text
            dry_text = self.default_text
            render_format = "HTML"
        # render text fot the consent component
        self.text = render_html_or_markdown(dry_text, render_format)
        self.title = title
        self.confirm = confirm
        self.deny = deny
