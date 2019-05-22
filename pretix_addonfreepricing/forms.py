from django import forms


class FreePriceField(forms.DecimalField):
    def clean(self, value):
        return str(value)
