from django import forms

from site_app.models import ContactInfo


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ["name", "email", "subject", "message"]

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control", "placeholder": field_name.capitalize()})
