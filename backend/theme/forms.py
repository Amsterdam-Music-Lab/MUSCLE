from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from .models import ThemeConfig
import json


class ColorPickerWidget(forms.widgets.Input):
    input_type = 'color'

    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'color-picker-widget'})

    def format_value(self, value):
        # Ensure the value is in the correct format for a color input (#RRGGBB)
        if value and not value.startswith('#'):
            value = '#' + value
        return value


class CustomColorWidget(forms.Widget):
    template_name = 'custom_color_widget.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = {
            'name': name,
            'value': value or '',
            # Add more context variables as needed
        }
        return mark_safe(render_to_string(self.template_name, context))


class ThemeConfigForm(forms.ModelForm):

    teal = forms.CharField(widget=ColorPickerWidget(), max_length=20, required=False, label='Teal')
    yellow = forms.CharField(widget=ColorPickerWidget(), max_length=20, required=False, label='Yellow')
    pink = forms.CharField(widget=ColorPickerWidget(), max_length=20, required=False, label='Pink')
    red = forms.CharField(widget=ColorPickerWidget(), max_length=20, required=False, label='Red')
    blue = forms.CharField(widget=ColorPickerWidget(), max_length=20, required=False, label='Blue')
    green = forms.CharField(widget=ColorPickerWidget(), max_length=20, required=False, label='Green')
    indigo = forms.CharField(widget=ColorPickerWidget(), max_length=20, required=False, label='Indigo')
    gray = forms.CharField(widget=ColorPickerWidget(), max_length=20, required=False, label='Gray')
    gray_900 = forms.CharField(widget=ColorPickerWidget(), max_length=20, required=False, label='Gray 900')
    black = forms.CharField(widget=ColorPickerWidget(), max_length=20, required=False, label='Black')

    primary = forms.CharField(widget=CustomColorWidget(), required=False, label='Primary')
    success = forms.CharField(widget=CustomColorWidget(), required=False, label='Success')
    positive = forms.CharField(widget=CustomColorWidget(), required=False, label='Positive')
    negative = forms.CharField(widget=CustomColorWidget(), required=False, label='Negative')
    secondary = forms.CharField(widget=CustomColorWidget(), required=False, label='Secondary')
    info = forms.CharField(widget=CustomColorWidget(), required=False, label='Info')

    class Meta:
        model = ThemeConfig
        exclude = ['css_variables']  # Exclude the original css_variables field
        fields = '__all__'
        widgets = {
            'css_variables': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'additional_variables': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'global_css': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

    class Media:
        js = ['color_picker.js', 'img_preview.js', 'font_preview.js']
        css = {"all": ["theme_admin.css"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default values for the color pickers
        self.fields['teal'].initial = '#39d7b8'
        self.fields['yellow'].initial = '#ffb14c'
        self.fields['pink'].initial = '#d843e2'
        self.fields['red'].initial = '#fa5577'
        self.fields['blue'].initial = '#0cc7f1'
        self.fields['green'].initial = '#00b612'
        self.fields['indigo'].initial = '#2b2bee'
        self.fields['gray'].initial = '#bdbebf'
        self.fields['gray_900'].initial = '#212529'
        self.fields['black'].initial = '#212529'

        self.fields['primary'].initial = 'pink'
        self.fields['success'].initial = 'teal'
        self.fields['positive'].initial = 'teal'
        self.fields['negative'].initial = 'red'
        self.fields['secondary'].initial = 'gray_900'
        self.fields['info'].initial = 'blue'

        if self.instance.css_variables:
            try:
                variables = json.loads(self.instance.css_variables)
                self.fields['teal'].initial = variables.get('teal', '#39d7b8')
                self.fields['yellow'].initial = variables.get('yellow', '#ffb14c')
                self.fields['pink'].initial = variables.get('pink', '#d843e2')
                self.fields['red'].initial = variables.get('red', '#fa5577')
                self.fields['blue'].initial = variables.get('blue', '#0cc7f1')
                self.fields['green'].initial = variables.get('green', '#00b612')
                self.fields['indigo'].initial = variables.get('indigo', '#2b2bee')
                self.fields['gray'].initial = variables.get('gray', '#bdbebf')
                self.fields['gray_900'].initial = variables.get('gray_900', '#212529')
                self.fields['black'].initial = variables.get('black', '#212529')

                self.fields['primary'].initial = variables.get('primary', '#d843e2')
                self.fields['success'].initial = variables.get('success', '#39d7b8')
                self.fields['positive'].initial = variables.get('positive', '#39d7b8')
                self.fields['negative'].initial = variables.get('negative', '#fa5577')
                self.fields['secondary'].initial = variables.get('secondary', '#212529')
                self.fields['info'].initial = variables.get('info', '#0cc7f1')

            except json.JSONDecodeError:
                pass  # Handle error or leave empty if JSON is invalid

    def save(self, commit=True):
        instance = super().save(commit=False)
        variables = {
            'teal': self.cleaned_data['teal'],
            'yellow': self.cleaned_data['yellow'],
            'pink': self.cleaned_data['pink'],
            'red': self.cleaned_data['red'],
            'blue': self.cleaned_data['blue'],
            'green': self.cleaned_data['green'],
            'indigo': self.cleaned_data['indigo'],
            'gray': self.cleaned_data['gray'],
            'gray_900': self.cleaned_data['gray_900'],
            'black': self.cleaned_data['black'],
            'primary': self.cleaned_data['primary'],
            'success': self.cleaned_data['success'],
            'positive': self.cleaned_data['positive'],
            'negative': self.cleaned_data['negative'],
            'secondary': self.cleaned_data['secondary'],
            'info': self.cleaned_data['info'],
        }

        instance.css_variables = json.dumps(variables)

        if commit:
            instance.save()
        return instance

