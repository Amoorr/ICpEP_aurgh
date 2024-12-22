from django import forms
from .models import Product, Cart

class ProductForm(forms.ModelForm):
    TAG_CHOICES = [
        ('Pre-orderable', 'Pre-orderable'),
        ('Buyable', 'Buyable'),
    ]

    tag = forms.ChoiceField(choices=TAG_CHOICES, label="Tag")

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'tag', 'quantity', 'product_description']  # Removed product_image
        widgets = {
            'tag': forms.Select(attrs={'id': 'id_tag'}),
            'quantity': forms.NumberInput(attrs={'id': 'id_quantity', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.tag == 'Buyable':
            self.fields['quantity'].required = True
        else:
            self.fields['quantity'].required = False

    def clean(self):
        cleaned_data = super().clean()
        tag = cleaned_data.get('tag')
        quantity = cleaned_data.get('quantity')

        if tag == 'Buyable' and (quantity is None or quantity < 0):
            self.add_error('quantity', 'Quantity is required for Buyable products.')
        elif tag == 'Pre-orderable':
            cleaned_data['quantity'] = None  # Automatically clear quantity for Pre-orderable
        return cleaned_data

    
from .models import Product, ProductImage


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']


class OrderForm(forms.ModelForm):
    """
    This is the form presented when the students want to order a specific product.
    """
    class Meta:
        model = Cart
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }
        labels = {
            'quantity': 'Order Quantity',
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')

        # Check stock availability before finalizing the order
        if product and quantity:
            if product.quantity < quantity:
                self.add_error('quantity', 'Not enough stock available for the requested quantity.')
        return cleaned_data


class SearchCartForm(forms.Form):
    search_query = forms.CharField(required=False, label="Search by Student Name")
    acad_year = forms.IntegerField(required=False, label="Academic Year")
    acad_block = forms.CharField(required=False, label="Academic Block")