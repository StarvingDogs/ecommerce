from django import forms
from .models import ShippingInfo

class ShippingInfoForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ['address', 'city', 'postal_code', 'country', 'phone']
