from crispy_bulma.layout import HTML, Div, Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.urls import reverse

from .models import Joint


class AddJointForm(forms.Form):
    target_url = forms.URLField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target_url'].label = False
        self.helper = FormHelper()
        self.helper.attrs = {
            'hx-post': reverse('joints:shorten'),
            'hx-target': '#form-result',
        }
        self.helper.layout = Layout(
            Div(
                Div(
                    Field(
                        'target_url',
                        placeholder='https://example.com',
                        label=False,
                        css_class='is-primary',
                        autofocus=True,
                    ),
                    css_class='control is-expanded',
                ),
                Div(
                    HTML(
                        '<button type="submit" class="button is-primary"><i class="fa-solid fa-compress mr-1"></i> Acortar</button>'
                    ),
                    css_class='control',
                ),
                css_class='field has-addons',
            ),
        )

    def save(self, *args, **kwargs):
        return Joint.add_joint(self.cleaned_data['target_url'])
