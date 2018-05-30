
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import RegexValidator

# Create your models here.

class Author(models.Model):
    # required to associate Author model with User model (Important)
    user = models.OneToOneField(User, null=True, blank=True, on_delete = models.CASCADE)

    # additional fields
    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    contact = models.CharField(validators=[phone_regex], max_length=17) # validators should be a list
    email = models.EmailField(max_length=200, blank=True)
    address = models.CharField(max_length=700)
    brandName = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return ("id: "+str(self.id)+": "+self.name) 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Supplier, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('supplier_detail', args=[self.id, self.slug])

class Supplier_Ledger(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE)
    amount_paid = models.DecimalField(max_length=200, max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    # def __str__(self):
    #     return self.supplier

    def save(self, *args, **kwargs):
        self.slug = slugify(self.supplier)
        super(Supplier_Ledger, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('supplier_ledger_detail', args=[self.id, self.slug])   

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE)
    # product = models.ForeignKey(Product, on_delete = models.CASCADE)
    totalBill = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default = 0.0)
    discount = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default = 0.0)
    paidAmount = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default = 0.0)
    # balance = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default = 0)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
 
    # @property
    # def balance(self):
    #     return -(self.totalBill - self.discount) + self.paidAmount

    # def __str__(self):
    #     return self.product

    # def get_readonly_fields(self, request, obj=None):
    #     if obj is None:
    #         return ['headline ']
    #     return []
  

    def save(self, *args, **kwargs):
        self.slug = slugify(self.supplier)
        super(Purchase, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('purchase_detail', args=[self.id, self.slug])

class Product(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete = models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    # supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE)
    description = models.CharField(max_length=5000, blank=True)
    fix_value = models.CharField(max_length=200, default= '2532')
    barcode = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    colour = models.CharField(max_length=200, blank=True)
    cost = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default = 0)
    salePrice = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default = 0)
    quantity = models.IntegerField(default = 0)
    bill = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default = 0.0)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    # class Meta:
    #     unique_together = ["name", "supplier", "description", "brand", "colour", "cost", "salePrice", "quantity"]

    # @property
    # def barcode(self):
    #     return (self.fix_value+str(self.id)+str(int(self.salePrice)))

    def barcode_generated(self, *args, **kwargs):
        self.barcode = self.fix_value+str(self.id)+str(int(self.salePrice))
        super(Product, self).save(*args, **kwargs)
        return self.barcode

    # def snippet(self):
    #     self.barcode = self.fix_value+str(self.id)+str(int(self.salePrice))
    #     return self.barcode    
    

    # @property
    # def bill(self):
    #     return self.quantity * self.cost 

    def __str__(self):
        return ("id: "+str(self.id)+": "+self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])          

class Customer(models.Model):
    name = models.CharField(max_length=200) 
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    contact = models.CharField(validators=[phone_regex], max_length=17) # validators should be a list
    email = models.EmailField(max_length=200, blank=True)
    address = models.CharField(max_length=700)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return ("id: "+str(self.id)+": "+self.name); 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Customer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('customer_detail', args=[self.id, self.slug])

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    totalBill = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default = 0.0)
    receivedAmount = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default = 0.0)
    # balance = models.CharField(max_length=200, default=0)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    # @property
    # def balance(self):
    #     return -(self.totalBill - self.discount) + self.receivedAmount

    # def __str__(self):
    #     return self.product

    def save(self, *args, **kwargs):
        self.slug = slugify(self.customer)
        super(Sale, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sale_detail', args=[self.id, self.slug])

class Sale_Product(models.Model):
    sale = models.ForeignKey(Sale, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    barcode = models.IntegerField()
    price = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default = 0.0)
    quantity = models.IntegerField(default = 0)
    bill = models.DecimalField(max_length=200, max_digits=15, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)        
          

class Customer_Ledger(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    amount_received = models.DecimalField(max_length=200, max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return self.customer

    def save(self, *args, **kwargs):
        self.slug = slugify(self.customer)
        super(Customer_Ledger, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('customer_ledger_detail', args=[self.id, self.slug])

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return self.customer

    def save(self, *args, **kwargs):
        self.slug = slugify(self.customer)
        super(Invoice, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('invoice_detail', args=[self.id, self.slug])                            


# from django.db import models
# from django.core.validators import RegexValidator

# # Create your models here.
# class Product(models.Model):
#     class Meta:
#         verbose_name_plural = "product"

#     product_id = models.CharField(primary_key=True,max_length=20)
#     product_name = models.CharField(max_length=200)
#     product_description = models.CharField(max_length=5000, blank=True)
#     product_barcode = models.CharField(max_length=200)
#     product_brand = models.CharField(max_length=200)
#     product_colour = models.CharField(max_length=200, blank=True)
#     product_cost = models.CharField(max_length=200)
#     product_salePrice = models.CharField(max_length=200)
#     product_quantity = models.CharField(max_length=200)
#     product_bill = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add =True)
#     updated_at = models.DateTimeField(auto_now =True)
#     def __str__(self):
#         return self.product_name
      

# class Purchase(models.Model):
#     class Meta:
#         verbose_name_plural = "purchase"

#     purchase_id = models.CharField(primary_key=True,max_length=20)
#     supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE)
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)
#     purchase_totalBill = models.CharField(max_length=200)
#     purchase_discount = models.CharField(max_length=200)
#     purchase_paidAmount = models.CharField(max_length=200)
#     purchase_balance = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add =True)
#     updated_at = models.DateTimeField(auto_now =True)

#     def __str__(self):
#         return self.purchase_id       

# class Supplier_Ledger(models.Model):
#     class Meta:
#         verbose_name_plural = "supplier_ledger"

#     supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE)
#     amount_paid = models.CharField(max_length=200)
#     date = models.DateField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add =True)
#     updated_at = models.DateTimeField(auto_now =True)

#     def __str__(self):
#         return self.date 

# class Customer(models.Model):
#     class Meta:
#         verbose_name_plural = "customer"

#     customer_id = models.CharField(primary_key=True,max_length=20)
#     customer_name = models.CharField(max_length=200, blank=True)
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     customer_contact = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
#     customer_email = models.EmailField(max_length=200, blank=True)
#     customer_address = models.CharField(max_length=700, blank=True)
#     created_at = models.DateTimeField(auto_now_add =True)
#     updated_at = models.DateTimeField(auto_now =True)

#     def __str__(self):
#         return self.customer_name                        

# class Sale(models.Model):
#     class Meta:
#         verbose_name_plural = "sale"
#     sale_id = models.CharField(primary_key=True,max_length=20)
#     customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)
#     sale_totalBill = models.CharField(max_length=200)
#     sale_discount = models.CharField(max_length=200)
#     sale_receivedAmount = models.CharField(max_length=200)
#     sale_balance = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add =True)
#     updated_at = models.DateTimeField(auto_now =True)

#     def __str__(self):
#         return self.sale_id       

# class Customer_Ledger(models.Model):
#     class Meta:
#         verbose_name_plural = "customer_ledger"

#     customer = models.ForeignKey(Supplier, on_delete = models.CASCADE)
#     amount_received = models.CharField(max_length=200)
#     date = models.DateField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add =True)
#     updated_at = models.DateTimeField(auto_now =True)

#     def __str__(self):
#         return self.supplier_name        