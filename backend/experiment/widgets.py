from django.forms import TextInput

class MarkdownPreviewTextInput(TextInput):
    template_name = "widgets/markdown_preview_text_input.html"

    class Media:
        css = {"all": ["markdown_preview.css"]}
        js = ["markdown_preview.js"]