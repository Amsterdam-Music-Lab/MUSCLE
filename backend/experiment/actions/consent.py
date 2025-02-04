from os.path import splitext

from django.template.loader import render_to_string
from django.template import Template, Context
from django_markup.markup import formatter
from django.core.files import File

from typing import Literal

from .base_action import BaseAction


def get_render_format(url: str) -> Literal["HTML", "MARKDOWN"]:
    """
    Detect markdown file based on file extension

    Args:
        url: Url of the consent file

    Returns:
        File format of the consent file (HTML or MARKDOWN)

    """
    if splitext(url)[1] == ".md":
        return "MARKDOWN"
    return "HTML"


def render_html_or_markdown(dry_text: str, render_format: Literal["HTML", "MARKDOWN"]) -> str:
    """render html or markdown

    Args:
        dry_text (str): contents of a markdown or html file
        render_format (Literal["HTML", "MARKDOWN"]): type of contents, either 'HTML' or 'MARKDOWN'

    Returns:
        Content rendered to html.
    """

    if render_format == "HTML":
        template = Template(dry_text)
        context = Context()
        return template.render(context)
    if render_format == "MARKDOWN":
        return formatter(dry_text, filter_name="markdown")

    raise ValueError("Invalid render format. Must be either 'HTML' or 'MARKDOWN'.")


class Consent(BaseAction):  # pylint: disable=too-few-public-methods
    """Handles experiment consent form generation and rendering and provides the consent form data to the frontend.

    This class manages the display and processing of informed consent forms for experiments.
    It can handle consent text from multiple sources (file upload, URL template, or default text)
    and supports both HTML and Markdown formats.

    Args:
        text (File): A Django File object containing the consent form content. If provided,
            this takes precedence over the URL parameter.
        title (Optional[str]): The heading displayed above the consent form.
            Defaults to "Informed consent".
        confirm (Optional[str]): Text for the confirmation button. Defaults to "I agree".
        deny (Optional[str]): Text for the rejection button. Defaults to "Stop".
        url (Optional[str]): Template path to load consent content if no text file is provided.
            Supports both HTML (default) and Markdown files.

    Example:
        ```python
        consent = Consent(
            text=File(open("path/to/consent.md")),
            title="Informed consent",
            confirm="I agree",
            deny="Stop",
        )
        ```

    Note:
        - The text file is normally uploaded via the admin interface for the experiment, so most of the time (and by default) you will use an experiment's `translated_content.consent` file.
        - This component is used in conjunction with the frontend Consent.tsx component
        - HTML templates can use Django template language
        - Markdown files are automatically converted to HTML
        - Priority order for content: 1) uploaded file, 2) template URL, 3) default text
    """

    # default consent text, that can be used for multiple blocks
    view = "CONSENT"

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
    ) -> None:
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
