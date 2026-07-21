from django import forms
from .models import Communication


class CommunicationForm(forms.ModelForm):
    class Meta:
        model = Communication
        fields = [
            "customer_name",
            "email",
            "phone",
            "channel",
            "direction",
            "summary",
        ]

        widgets = {
            "customer_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter customer name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter email",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter phone number",
                }
            ),
            "channel": forms.Select(
                attrs={"class": "form-select"}
            ),
            "direction": forms.Select(
                attrs={"class": "form-select"}
            ),
            "summary": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Communication summary",
                }
            ),
        }