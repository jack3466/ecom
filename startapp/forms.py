from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList
class CartForm(forms.Form):
    quantity=forms.IntegerField(initial=1)
    product_id=forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self,request,*args,**kwargs):
        self.request=request
        super(CartForm,self).__init__(*args,**kwargs)
        