from django import forms
from django.core.exceptions import ValidationError
from .models import Author, Supplier, Supplier_Ledger, Product, Purchase, Customer, Sale, Customer_Ledger, Invoice, Sale_Product
from django.template.defaultfilters import slugify
# from django.forms.models import inlineformset_factory
# from django.forms.models import BaseInlineFormSet

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']
        name_l = name.lower()
        if name_l == "admin" or name_l == "author":
            raise ValidationError("Author name can't be 'admin/author'")
        return name

    def clean_email(self):
        return self.cleaned_data['email'].lower()


class SupplierForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Supplier
        fields = ('name', 'contact', 'email', 'address', 'brandName',)

    def clean_name(self):
        n = self.cleaned_data['name']
        if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
            raise ValidationError("Supplier name can't be '{}'".format(n))
        return n

    def clean(self):
        cleaned_data = super(SupplierForm, self).clean() # call the parent clean method
        name  = cleaned_data.get('name')
        # if title exists create slug from title
        if name:
            cleaned_data['slug'] = slugify(name)
        return cleaned_data  

class SupplierLedgerForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)
    def __init__(self, *args, **kwargs):
        super(SupplierLedgerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Supplier_Ledger
        fields = ('supplier', 'amount_paid',)

    def clean_name(self):
        n = self.cleaned_data['supplier']
        if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
            raise ValidationError("Supplier_Ledger name can't be '{}'".format(n))
        return n

    def clean(self):
        cleaned_data = super(SupplierLedgerForm, self).clean() # call the parent clean method
        supplier  = cleaned_data.get('supplier')
        # if title exists create slug from title
        if supplier:
            cleaned_data['slug'] = slugify(supplier)
        return cleaned_data                                               

class PurchaseForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
       super(PurchaseForm, self).__init__(*args, **kwargs)
       self.fields['totalBill'].widget.attrs['readonly'] = True
       for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control calculate' 

    # def __init__(self, *args, **kwargs):
    #     super(PurchaseForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control calculate'   

    class Meta:
        model = Purchase
        fields = ('supplier', 'totalBill', 'discount', 'paidAmount',)

    def clean_name(self):
        n = self.cleaned_data['supplier']
        if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
            raise ValidationError("Purchase name can't be '{}'".format(n))
        return n

    # def clean(self):
    #     cleaned_data = super(PurchaseForm, self).clean() # call the parent clean method
    #     product  = cleaned_data.get('supplier')
    #     # if title exists create slug from title
    #     if product:
    #         cleaned_data['slug'] = slugify(supplier)
    #     return cleaned_data     

class ProductForm(forms.ModelForm):
    # author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
       super(ProductForm, self).__init__(*args, **kwargs)
       self.fields['bill'].widget.attrs['readonly'] = True
       for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control calculate' 

    class Meta:
        model = Product
        fields = ('name', 'description', 'brand', 'colour', 'cost', 'salePrice', 'quantity', 'bill')
        exclude = ('purchase',)

    def clean_name(self):
        n = self.cleaned_data['name']
        if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
            raise ValidationError("Supplier_Ledger name can't be '{}'".format(n))
        return n

    def clean(self):
        cleaned_data = super(ProductForm, self).clean() # call the parent clean method
        name  = cleaned_data.get('name')
        # if title exists create slug from title
        if name:
            cleaned_data['slug'] = slugify(name)
        return cleaned_data

    # def clean(self):
    # if 'newsletter_sub' in self.data:
    #     # do subscribe
    # elif 'newsletter_unsub' in self.data:
    #     # do unsubscribe 

# ProductMemberFormSet = inlineformset_factory(Purchase, Product, form=ProductForm, extra=1)

class CustomerForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Customer
        fields = ('name', 'contact', 'email', 'address',)

    def clean_name(self):
        n = self.cleaned_data['name']
        if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
            raise ValidationError("Customer name can't be '{}'".format(n))
        return n

    def clean(self):
        cleaned_data = super(CustomerForm, self).clean() # call the parent clean method
        name  = cleaned_data.get('name')
        # if title exists create slug from title
        if name:
            cleaned_data['slug'] = slugify(name)
        return cleaned_data        

class SaleForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
       super(SaleForm, self).__init__(*args, **kwargs)
       self.fields['totalBill'].widget.attrs['readonly'] = True
       for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control calculate' 

    class Meta:
        model = Sale
        fields = ('customer', 'totalBill', 'discount', 'receivedAmount',)

    def clean_name(self):
        n = self.cleaned_data['customer']
        if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
            raise ValidationError("Sale name can't be '{}'".format(n))
        return n

    def clean(self):
        cleaned_data = super(SaleForm, self).clean() # call the parent clean method
        customer  = cleaned_data.get('customer')
        # if title exists create slug from title
        if customer:
            cleaned_data['slug'] = slugify(customer)
        return cleaned_data          

class SaleProductForm(forms.ModelForm):
    # author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(SaleProductForm, self).__init__(*args, **kwargs)
        self.fields['bill'].widget.attrs['readonly'] = True
        self.fields['barcode'].widget.attrs['placeholder'] = 'Enter Product Barcode...'
        # self.fields['barcode'].widget.attrs['onkeyup'] = 'check()'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control calculate'

    class Meta:
        model = Sale_Product
        fields = ('product', 'barcode', 'price', 'quantity', 'bill')
        exclude = ('sale',)

    def clean_name(self):
        n = self.cleaned_data['product']
        if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
            raise ValidationError("Sale name can't be '{}'".format(n))
        return n

    def clean(self):
        cleaned_data = super(SaleProductForm, self).clean() # call the parent clean method
        product  = cleaned_data.get('product')
        # if title exists create slug from title
        if product:
            cleaned_data['slug'] = slugify(product)
        return cleaned_data

class CustomerLedgerForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(CustomerLedgerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Customer_Ledger
        fields = ('customer', 'amount_received',)

    def clean_name(self):
        n = self.cleaned_data['customer']
        if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
            raise ValidationError("Customer Ledger name can't be '{}'".format(n))
        return n

    def clean(self):
        cleaned_data = super(CustomerLedgerForm, self).clean() # call the parent clean method
        customer  = cleaned_data.get('customer')
        # if title exists create slug from title
        if customer:
            cleaned_data['slug'] = slugify(customer)
        return cleaned_data                         

class InvoiceForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Invoice
        fields = ('customer',)

    def clean_name(self):
        n = self.cleaned_data['customer']
        if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
            raise ValidationError("Customer Ledger name can't be '{}'".format(n))
        return n

    def clean(self):
        cleaned_data = super(InvoiceForm, self).clean() # call the parent clean method
        customer  = cleaned_data.get('customer')
        # if title exists create slug from title
        if customer:
            cleaned_data['slug'] = slugify(customer)
        return cleaned_data       