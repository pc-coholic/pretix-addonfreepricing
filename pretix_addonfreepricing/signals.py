import json
from decimal import Decimal

from django import forms
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from pretix.presale.signals import (
    fee_calculation_for_cart, question_form_fields,
)
from pretix.presale.views import get_cart

from .forms import FreePriceField


@receiver(question_form_fields, dispatch_uid='addonfreepricing_question_form_fields')
def question_form_fields(sender, position, **kwargs):

    if position.addon_to:
        return {
            'price': FreePriceField(
                label=_("Price"),
                max_digits=7, decimal_places=2, required=True,
                localize=True,
                widget=forms.NumberInput(
                    attrs={
                        'placeholder': position.item.default_price,
                        'value': position.item.default_price,
                        'addon_before': position.item.event.currency,
                        'decimal_places': 2,
                        'min': position.item.default_price
                    }
                ),
            )
        }

    return {}

# Hackhackhack
@receiver(fee_calculation_for_cart, dispatch_uid="addonfreepricing_fee_calculation_for_cart")
def fee_calculation_for_cart(sender, request, invoice_address, total, **kwargs):
    cart = get_cart(request)

    for position in cart:
        if position.addon_to:
            if position.item.free_price:
                meta_info = json.loads(position.meta_info or '{}')

                if 'question_form_data' in meta_info:
                    if 'price' in meta_info['question_form_data']:
                        if Decimal(meta_info['question_form_data']['price']) >= position.item.default_price:
                            position.price = Decimal(meta_info['question_form_data']['price'])
                        else:
                            position.price = position.item.default_price

                        position.save()

    return []
