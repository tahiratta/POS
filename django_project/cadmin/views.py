from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404, HttpResponse
from blog.forms import SupplierForm, SupplierLedgerForm, ProductForm, PurchaseForm, CustomerForm, SaleForm, CustomerLedgerForm, InvoiceForm, SaleProductForm 
from django.contrib import messages
from blog.models import Author, Supplier, Supplier_Ledger, Product, Purchase, Customer, Sale, Customer_Ledger, Invoice, Sale_Product
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django_project import helpers
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from blog.mybarcode import MyBarcodeDrawing
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext  # For CSRF
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect
from blog.forms import *
# from dynamicform.todo.forms import *
# from django.views.generic.base import TemplateView
# import json
# import simplejson as json
# from decimal import Decimal

# from django import template
# from django.template.Library.filter()
# Create your views here.

# register = template.Library()

# @register.filter(name='subtract')
# def subtract(value, arg):
#     return value - arg

@login_required
def home(request):
    return render(request, 'cadmin/admin_page.html')

def barcode(request):
    products = Product.objects.order_by("-id").all()
    #instantiate a drawing object
    # import mybarcod
    for product in products:
        d = MyBarcodeDrawing(product.barcode)
        binaryStuff = d.asString('jpg')
    return HttpResponse(binaryStuff, 'image/jpg')   

@login_required
def invoice_show(request, pk=None):
    # customer = get_object_or_404(Customer, pk=pk)
    if request.user.is_superuser:
        if pk:
            customer = Customer.objects.get(pk=pk)
            invoices = Invoice.objects.order_by("-id").all()
            # invoices = Invoice.objects.get(pk=self.kwargs.get('pk'))
            # invoices = Invoice.objects.Invoice.objects.get(pk=pk)
            customers = Customer.objects.order_by("-id").all()
            customer_ledgers = Customer_Ledger.objects.order_by("-id").all()
            sales = Sale.objects.order_by("-id").all()
            products = Product.objects.order_by("-id").all()
            sale_products = Sale_Product.objects.order_by("-id").all()
            total_amount = 0
            total_discount = 0
            customer_id=customer.id
            total_balance = 0
            for product in products:
                for sale in sales:
                    for customer in customers:
                        for sale_product in sale_products:
                            if customer_id == customer.id:
                                if customer.id == sale.customer.id:
                                    if sale_product.sale.id == sale.id:
                                        total_amount = total_amount + sale.totalBill
                                        total_discount = sale.discount
                                        total_balance = (-(sale.totalBill-sale.discount)+sale.receivedAmount) 

                                        # for customer_ledger in customer_ledgers: 
                                        #     if sale.customer.id == customer_ledger.customer.id:
                                        #         total_balance = total_balance + (-(product.bill-sale.discount)+customer_ledger.amount_received) 
                                

            # query = request.GET.get("q")
            # if query:
            #     suppliers = suppliers.filter(
            #         Q(id__icontains=query) 
            #         # Q(name__icontains=query) |
            #         # Q(contact__icontains=query) |
            #         # Q(email__icontains=query) |
            #         # Q(address__icontains=query) |
            #         # Q(brandName__icontains=query) |
            #         # Q(created_at__icontains=query)  
            #         ).distinct()
    else:
        invoices = Invoice.objects.filter(author__user__username=request.user.username).order_by("-id")
        customers = Customer.objects.filter(author__user__username=request.user.username).order_by("-id")
        customer_ledgers = Customer_Ledger.objects.filter(author__user__username=request.user.username).order_by("-id")
        sales = Sale.objects.filter(author__user__username=request.user.username).order_by("-id")
        products = Products.objects.filter(author__user__username=request.user.username).order_by("-id")

        # invoices = helpers.pg_records(request, invoices, 5)    
        # customers = helpers.pg_records(request, customers, 5)
        # customer_ledgers = helpers.pg_records(request, customer_ledgers, 5)
        # sales = helpers.pg_records(request, sales, 5)
        # products = helpers.pg_records(request, products, 5)

    return render(request, 'cadmin/invoice_show.html', {'invoices': invoices, 'customer_id':customer_id , 'total_amount':total_amount, 'total_discount':total_discount, 'total_balance':total_balance, 'customers': customers, 'customer_ledgers': customer_ledgers, 'sales': sales, 'products': products, 'sale_products': sale_products})    


# @login_required
# def invoice_add(request):
#     # If request is POST, create a bound form(form with data)
#     if request.method == "POST":
#         f = SupplierForm(request.POST)

#         # check whether form is valid or not
#         # if the form is valid, save the data to the database
#         # and redirect the user back to the add post form

#         # If form is invalid show form with errors again
#         if f.is_valid():
#             # if author is not selected and user is superuser, then assign the post to the author named staff
#             if request.POST.get('author') == "" and request.user.is_superuser:
#                 new_supplier = f.save(commit=False)
#                 author = Author.objects.get(user__username='staff')
#                 new_supplier.author = author
#                 new_supplier.save()
#                 f.save_m2m()

#             # if author is selected and user is superuser
#             elif request.POST.get('author') and request.user.is_superuser:
#                 new_supplier = f.save()

#             # if user is not a superuser
#             else:
#                 new_supplier = f.save(commit=False)
#                 # new_supplier.author = Author.objects.get(user__username=request.user.username)
#                 new_supplier.save()
#                 f.save_m2m()

#             messages.add_message(request, messages.INFO, 'Invoice added.')
#             return redirect('customer_list')

#     # if request is GET the show unbound form to the user
#     else:
#         f = SupplierForm()
#     return render(request, 'cadmin/invoice.html', {'form': f})

def login(request, **kwargs):
    if request.user.is_authenticated:
        return redirect('/cadmin/')
    else:
        return auth_views.login(request, **kwargs)


def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            # send email verification now
            activation_key = helpers.generate_activation_key(username=request.POST['username'])

            subject = "TheGreatDjangoBlog Account Verification"

            message = '''\n
            Please visit the following link to verify your account \n\n{0}://{1}/cadmin/activate/account/?key={2}
                                    '''.format(request.scheme, request.get_host(), activation_key)

            error = False

            try:
                send_mail(subject, message, settings.SERVER_EMAIL, [request.POST['email']])
                messages.add_message(request, messages.INFO,
                                     'Account created! Click on the link sent to your email to activate the account')

            except:
                error = True
                messages.add_message(request, messages.INFO, 'Unable to send email verification. Please try again')

            if not error:
                u = User.objects.create_user(
                    request.POST['username'],
                    request.POST['email'],
                    request.POST['password1'],
                    is_active=0,
                    is_staff=True
                )

                author = Author()
                author.activation_key = activation_key
                author.user = u
                author.save()

            return redirect('register')

    else:
        f = CustomUserCreationForm()

    return render(request, 'cadmin/register.html', {'form': f})


def activate_account(request):
    key = request.GET['key']
    if not key:
        raise Http404()

    r = get_object_or_404(Author, activation_key=key, email_validated=False)
    r.user.is_active = True
    r.user.save()
    r.email_validated = True
    r.save()

    return render(request, 'cadmin/activated.html')


@login_required
def account_info(request):
    return render(request, 'cadmin/account_info.html')

#----------------------------------------------------------------------------#
# If i remove these two views it gives me error what's wrong with these views
@login_required
def category_list(request):
        return render(request, 'cadmin/category_list.html')        

@login_required
def tag_list(request):
    return render(request, 'cadmin/tag_list.html') 
# See them later  
#------------------------------------------------------------------------------#     
@login_required
def index(request):
    # response = HttpResponseRedirect('purchase/product/add/')
    # response = HttpResponseRedirect('')
    # response.delete_cookie('list_ids')
    # print(request.COOKIES.get('list_ids'))
    # return response

    # if request.COOKIES.get('list_ids'):
    #    response = HttpResponse("Cookies Cleared")
    #    response.delete_cookie("list_ids")
    #    print(request.COOKIES.get('list_ids'))
    #    return response


    if request.user.is_superuser:
        suppliers = Supplier.objects.order_by("-id").all()
        purchases = Purchase.objects.order_by("-id").all()
        sales = Sale.objects.order_by("-id").all()
        customers = Customer.objects.order_by("-id").all()

    else:
        suppliers = Supplier.objects.filter(author__user__username=request.user.username).order_by("-id")
        purchases = Purchase.objects.filter(author__user__username=request.user.username).order_by("-id")
        sales = Sale.objects.filter(author__user__username=request.user.username).order_by("-id")
        customers = Customer.objects.filter(author__user__username=request.user.username).order_by("-id")

    suppliers = helpers.pg_records(request, suppliers, 5)
    purchases = helpers.pg_records(request, purchases, 5)
    sales = helpers.pg_records(request, sales, 5)
    customers = helpers.pg_records(request, customers, 5)

    return render(request, 'cadmin/index.html', {'suppliers': suppliers, 'customers': customers, 'sales': sales, 'purchases': purchases})

@login_required
def supplier_view(request, pk=None):
    if request.user.is_superuser:
        if pk:
            supplier = Supplier.objects.get(pk=pk)
            suppliers = Supplier.objects.order_by("-id").all()
            purchases = Purchase.objects.order_by("-id").all()
            supplier_ledgers = Supplier_Ledger.objects.order_by("-id").all()
            products = Product.objects.order_by("-id").all()

            total_business = 0
            total_balance = 0
            total_payment = 0
            total_amountPaid = 0
            supplier_id=supplier.id
            for purchase in purchases:
                for product in products:
                    for supplier in suppliers:
                        if supplier_id == supplier.id:
                            if supplier.id == purchase.supplier.id: 
                                if product.purchase.id == purchase.id:                   
                                    total_business = total_business + purchase.totalBill
                                    total_payment = total_payment + purchase.totalBill
                                    total_balance = total_balance + (-(purchase.totalBill)+purchase.paidAmount)
                                    total_amountPaid = purchase.paidAmount 
                                    # for supplier_ledger in supplier_ledgers: 
                                    #     if purchase.supplier.id == supplier_ledger.supplier.id:
                                    #         total_balance = total_balance + (-(product.bill-purchase.discount)+supplier_ledger.amount_paid)
                                    #         total_amountPaid = supplier_ledger.amount_paid 


                                            

    return render(request, 'cadmin/supplier_view.html', {'suppliers': suppliers, 'supplier_id': supplier_id, 'purchases': purchases, 'supplier_ledgers': supplier_ledgers, 'products': products, 'total_business':total_business, 'total_balance':total_balance, 'total_amountPaid':total_amountPaid, 'total_payment':total_payment})


# @login_required
# def supplier_view(request):
#     suppliers = Supplier.objects.order_by("-id").all()
#     purchases = Purchase.objects.order_by("-id").all()
#     supplier_ledgers = Supplier_Ledger.objects.order_by("-id").all()
#     products = Product.objects.order_by("-id").all()

#     total_business = 0
#     total_balance = 0
#     total_amountPaid = 0
#     total_payment = 0
#     for purchase in purchases:
#         for product in products: 
#             total_payment = total_payment + product.bill
#             if purchase.product.id == product.id:                    
#                 total_business = total_business + product.bill
#                 total_balance = total_balance + purchase.balance

#                 for supplier_ledger in supplier_ledgers: 
#                     if purchase.supplier.id == supplier_ledger.supplier.id:
#                         total_balance = total_balance + (-(product.bill-purchase.discount)+supplier_ledger.amount_paid) 
#                         total_amountPaid = total_amountPaid + supplier_ledger.amount_paid

#     return render(request, 'cadmin/supplier_view.html', {'suppliers': suppliers, 'purchases': purchases, 'supplier_ledgers': supplier_ledgers, 'products': products, 'total_business':total_business, 'total_balance':total_balance, 'total_amountPaid':total_amountPaid, 'total_payment':total_payment})

@login_required
def supplier_list(request):
    if request.user.is_superuser:
        suppliers = Supplier.objects.order_by("-id").all()
        query = request.GET.get("q")
        if query:
            suppliers = suppliers.filter(
                Q(id__icontains=query) 
                # Q(name__icontains=query) |
                # Q(contact__icontains=query) |
                # Q(email__icontains=query) |
                # Q(address__icontains=query) |
                # Q(brandName__icontains=query) |
                # Q(created_at__icontains=query)  
                ).distinct()
    else:
        suppliers = Supplier.objects.filter(author__user__username=request.user.username).order_by("-id")

    suppliers = helpers.pg_records(request, suppliers, 5)

    return render(request, 'cadmin/supplier_list.html', {'suppliers': suppliers})

@login_required
def supplier_add(request):
    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = SupplierForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                new_supplier = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_supplier.author = author
                new_supplier.save()
                f.save_m2m()

            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                new_supplier = f.save()

            # if user is not a superuser
            else:
                new_supplier = f.save(commit=False)
                # new_supplier.author = Author.objects.get(user__username=request.user.username)
                new_supplier.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Supplier added.')
            return redirect('purchase_add')

    # if request is GET the show unbound form to the user
    else:
        f = SupplierForm()
    return render(request, 'cadmin/supplier_add.html', {'form': f})

@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = SupplierForm(request.POST, instance=supplier)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_supplier = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_supplier.author = author
                updated_supplier.save()
                f.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_supplier = f.save()
            # if user is not a superuser
            else:
                updated_supplier = f.save(commit=False)
                # updated_supplier.author = Author.objects.get(user__username=request.user.username)
                updated_supplier.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Supplier updated.')
            return redirect(reverse('purchase_add'))

    # if request is GET the show unbound form to the user, along with data
    else:
        f = SupplierForm(instance=supplier)

    return render(request, 'cadmin/supplier_update.html', {'form': f, 'supplier': supplier})

@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Supplier deleted')
    return redirect(next_page)


@login_required
def supplier_ledger_list(request):
    if request.user.is_superuser:
        supplier_ledgers = Supplier_Ledger.objects.order_by("-id").all()
        query = request.GET.get("q")
        if query:
            supplier_ledgers = supplier_ledgers.filter(
                Q(id__icontains=query) 
                # Q(supplier__icontains=query) |
                # Q(amount_paid__icontains=query) |
                # Q(created_at__icontains=query) 
                ).distinct()
    else:
        supplier_ledgers = Supplier_Ledger.objects.filter(author__user__username=request.user.username).order_by("-id")

    supplier_ledgers = helpers.pg_records(request, supplier_ledgers, 5)

    return render(request, 'cadmin/supplier_ledger_list.html', {'supplier_ledgers': supplier_ledgers})

@login_required
def supplier_ledger_add(request):
    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = SupplierLedgerForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                new_supplier_ledger = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_supplier_ledger.author = author
                new_supplier_ledger.save()
                f.save_m2m()

            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                new_supplier_ledger = f.save()

            # if user is not a superuser
            else:
                new_supplier_ledger = f.save(commit=False)
                # new_supplier_ledger.author = Author.objects.get(user__username=request.user.username)
                new_supplier_ledger.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Supplier_Ledgers added.')
            return redirect('supplier_ledger_list')

    # if request is GET the show unbound form to the user
    else:
        f = SupplierLedgerForm()
    return render(request, 'cadmin/supplier_ledger_add.html', {'form': f})

@login_required
def supplier_ledger_update(request, pk):
    supplier_ledger = get_object_or_404(Supplier_Ledger, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = SupplierLedgerForm(request.POST, instance=supplier_ledger)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_supplier_ledger = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_supplier_ledger.author = author
                updated_supplier_ledger.save()
                f.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_supplier_ledger = f.save()
            # if user is not a superuser
            else:
                updated_supplier_ledger = f.save(commit=False)
                # updated_supplier_ledger.author = Author.objects.get(user__username=request.user.username)
                updated_supplier_ledger.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Supplier_Ledger updated.')
            # return redirect(reverse('supplier_ledger_update', args=[supplier_ledger.id]))
            return redirect(reverse('supplier_ledger_list'))

    # if request is GET the show unbound form to the user, along with data
    else:
        f = SupplierLedgerForm(instance=supplier_ledger)

    return render(request, 'cadmin/supplier_ledger_update.html', {'form': f, 'supplier_ledger': supplier_ledger})

@login_required
def supplier_ledger_delete(request, pk):
    supplier_ledger = get_object_or_404(Supplier_Ledger, pk=pk)
    supplier_ledger.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Supplier_Ledger deleted')
    return redirect(next_page)  

@login_required
def purchase_list(request):
    if request.user.is_superuser:
        count = 0
        purchases = Purchase.objects.order_by("-id").all()
        products = Product.objects.order_by("-id").all()
        supplier_ledgers = Supplier_Ledger.objects.order_by("-id").all()
        for product in products:
            if 'supplier.id' in request.session:
                supplier_id = request.session['supplier.id']
                print(supplier_id)           
        # total_amountPaid = purchase_product_add(total_amountPaid)
        if 'total_amountPaid' in request.session:
            total_amountPaid = request.session['total_amountPaid']
            # total_amountPaid = Decimal(total_amountPaid)
        if 'total_bill' in request.session:
            total_bill = request.session['total_bill']
            # total_bill = Decimal(total_bill1)
        if 'total_balance' in request.session:
            total_balance = request.session['total_balance']
            # total_balance = Decimal(total_balance1)
        if 'total_supplier' in request.session:
            total_supplier = request.session['total_supplier']
        total_amountPaid = request.COOKIES.get('total_amountPaid')
        total_bill = request.COOKIES.get('total_bill')
        total_balance = request.COOKIES.get('total_balance')
        total_supplier = request.COOKIES.get('total_supplier')

        query = request.GET.get("q")
        if query:
            purchases = purchases.filter(
                Q(id__icontains=query) 
                # Q(supplier__icontains=query) |
                # Q(product__icontains=query) |
                # Q(totalBill__icontains=query) |
                # Q(discount__icontains=query) |
                # Q(paidAmount__icontains=query) |
                # Q(balance__icontains=query) |
                # Q(temp__icontains=query) |
                # Q(created_at__icontains=query)  
                ).distinct()                

    else:
        purchases = Purchase.objects.filter(author__user__username=request.user.username).order_by("-id")
        products = Product.objects.filter(author__user__username=request.user.username).order_by("-id")
        supplier_ledgers = Supplier_Ledger.objects.filter(author__user__username=request.user.username).order_by("-id")
   
    purchases = helpers.pg_records(request, purchases, 15)
    products = helpers.pg_records(request, products, 15)
    supplier_ledgers = helpers.pg_records(request, supplier_ledgers, 15)
         
    return render(request, 'cadmin/purchase_list.html', {'total_amountPaid': total_amountPaid,'total_bill': total_bill, 'total_balance': total_balance, 'total_supplier': total_supplier, 'purchases': purchases,'products': products, 'supplier_ledgers' : supplier_ledgers})

# class AddProductView(generic.TemplateView):
#     template_name = 'cadmin/purchase_add.html'

#     def get(self, request, *args, **kwargs):
#         purchase_form = PurchaseForm(self.request.GET or None, prefix="purch")
#         product_form = ProductForm(self.request.GET or None, prefix="prod")
#         context = super(AddProductView, self).get_context_data(**kwargs)
#         context['purchase_form'] = purchase_form
#         context['product_form'] = product_form
#         return self.render_to_response(context)

# class PurchaseCreateView(CreateView):
#     model = Purchase

#     def form_valid(self, form):
#         result = super(PurchaseCreateView, self).form_valid(form)

#         products_formset = ProductInlineFormSet(form.data, instance=self.object, prefix='products_formset')
#         if products_formset.is_valid():
#             products = products_formset.save()

#         products_count = 0
#         return result

#     def get_context_data(self, **kwargs):
#         context = super(PurchaseCreateView, self).get_context_data(**kwargs)
#         context['products_formset'] = ProductInlineFormSet(prefix='products_formset')
#         return context

@login_required
def purchase_add(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False
    ProductFormSet = formset_factory(ProductForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST': # If the form has been submitted...
        purchase_form = PurchaseForm(request.POST) # A form bound to the POST data
        # print(purchase_form)
        # Create a formset from the submitted data
        product_formset = ProductFormSet(request.POST, request.FILES)
        # print(product_formset)

        if purchase_form.is_valid() and product_formset.is_valid():
            purchase = purchase_form.save()
            for form in product_formset.forms:
                print(product_formset)
                product = form.save(commit=False)
                product.purchase = purchase
                product.save()
            return redirect('purchase_list') # Redirect to a 'success' page
    else:
        purchase_form = PurchaseForm()
        product_formset = ProductFormSet()

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'purchase_form': purchase_form,
         'product_formset': product_formset,
        }
    c.update(csrf(request))

    return render_to_response('cadmin/purchase_add.html', c)

    # purchase_form = PurchaseForm()
    # product_form = ProductForm()
    # # If request is POST, create a bound form(form with data)
    # if request.method == "POST":
    #     purchase_form = PurchaseForm(request.POST)
    #     product_form = ProductForm(request.POST)
    #     print(purchase_form)
    #     print(product_form)

    #     # check whether form is valid or not
    #     # if the form is valid, save the data to the database
    #     # and redirect the user back to the add post form

    #     # If form is invalid show form with errors again
    #     if purchase_form.is_valid() or product_form.is_valid():
    #         new_purchase = purchase_form.save(commit=False)
    #         print(purchase_form)
    #         # new_customer.author = Author.objects.get(user__username=request.user.username)
    #         new_purchase.save()
    #         print(new_purchase.id) 
    #         purchase_form.save_m2m()

    #         messages.add_message(request, messages.INFO, 'Purchase added.')

    #         new_product = product_form.save(commit=False)
    #         # new_customer.author = Author.objects.get(user__username=request.user.username)
    #         new_product.save()
    #         print(new_product.name) 
    #         product_form.save_m2m()

    #         messages.add_message(request, messages.INFO, 'Product added.')
    #         return redirect('purchase_add')

    # # if request is GET the show unbound form to the user
    # else:
    #     purchase_form = PurchaseForm()
    #     product_form = ProductForm()
    # return render(request, 'cadmin/purchase_add.html', {'form1': purchase_form, 'form': product_form })














    # # If request is POST, create a bound form(form with data)
    # # if request.method == "POST":
    # if "purchase" in request.POST:
    #     purchase_form = PurchaseForm(request.POST)
    #     print(purchase_form)
    #     # check whether form is valid or not
    #     # if the form is valid, save the data to the database
    #     # and redirect the user back to the add post form

    #     # If form is invalid show form with errors again

    #     if purchase_form.is_valid():

    #         new_purchase = purchase_form.save(commit=False)
    #         # new_purchase.author = Author.objects.get(user__username=request.user.username)
    #         new_purchase.save()
    #         purchase_form.save_m2m()
    #         messages.add_message(request, messages.INFO, 'Purchases added.')
    #         # return redirect('purchase_add')
    # else:
    #     purchase_form = PurchaseForm()

    # if "product" in request.POST:        
    #     product_form = ProductForm(request.POST)
    #     if product_form.is_valid():
    #         new_product = product_form.save(commit=False)
    #         # new_product.author = Author.objects.get(user__username=request.user.username)
    #         new_product.save()
    #         product_form.save_m2m()
    #         messages.add_message(request, messages.INFO, 'Products added.')
    #         # return redirect('product_add')
    # else:
    #     product_form = ProductForm()    

    # #if request is GET the show unbound form to the user
    # return render(request, 'cadmin/purchase_add.html', {'form1': purchase_form, 'form': product_form})

    # # Initalize our two forms here with separate prefixes
    # purchase_form = PurchaseForm(prefix="purch")
    # product_form = ProductForm(prefix="prod")

    # # Check to see if a POST has been submitted. Using GET to submit forms?
    # # Don't do it. Use POST.
    # if request.POST:
    #     # Load up our two forms again using the prefix keyword argument.
    #     purchase_form = PurchaseForm(request.POST, prefix="purch")
    #     product_form = ProductForm(request.POST, prefix="prod")

    #     # Ensure both forms are valid before continuing on
    #     if purchase_form.is_valid() and product_form.is_valid():
    #         # Prepare the school model, but don't commit it to the database
    #         # just yet
    #         purchase = purchase_form.save(commit=False)
    #         # Add the location ForeignKey by saving the secondary form we
    #         # setup
    #         product = product_form.save(commit=False)

    #         # Save the main object and continue on our merry way.
    #         purchase.save()
    #         print(purchase.totalBill) 
    #         product.save()
    #         # return _goto_school(purchase)
    # return render(request, 'cadmin/purchase_add.html', {'form1': purchase_form, 'form': product_form})

@login_required
def purchase_update(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = PurchaseForm(request.POST, instance=purchase)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_purchase = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_purchase.author = author
                updated_purchase.save()
                f.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_purchase = f.save()
            # if user is not a superuser
            else:
                updated_purchase = f.save(commit=False)
                # updated_purchase.author = Author.objects.get(user__username=request.user.username)
                updated_purchase.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Purchase updated.')
            return redirect(reverse('purchase_update', args=[purchase.id]))

    # if request is GET the show unbound form to the user, along with data
    else:
        f = PurchaseForm(instance=purchase)

    return render(request, 'cadmin/purchase_update.html', {'form': f, 'purchase': purchase})

@login_required
def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    purchase.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Purchase deleted')
    return redirect(next_page)  

@login_required
def product_view(request):
    if request.user.is_superuser:
        products = Product.objects.order_by("-id").all()
        supplier_ledgers = Supplier_Ledger.objects.order_by("-id").all()
        suppliers = Supplier.objects.order_by("-id").all()
        stock_amount = 0
        total_brands = 0
        for supplier_ledger in supplier_ledgers:
            stock_amount = stock_amount + supplier_ledger.amount_paid
        for supplier in suppliers:
            supplier.brandName = supplier.brandName
            total_brands = total_brands + 1  
        # for product in products:
        # product.barcode = product.fix_value + product.salePrice + product.id 
        query = request.GET.get("q")
        if query:
            products = products.filter(
                Q(supplier__name__contains=query) |
                Q(supplier__id__contains=query)
                # Q(name__icontains=query) |
                # Q(description__icontains=query) |
                # Q(fix_value__icontains=query) |
                # Q(barcode__icontains=query) |
                # Q(colour__icontains=query) |
                # Q(cost__icontains=query) |
                # Q(salePrice__icontains=query) |
                # Q(quantity__icontains=query) |
                # Q(bill__icontains=query) |
                # Q(created_at__icontains=query)  
                ).distinct()

    else:
        products = Product.objects.filter(author__user__username=request.user.username).order_by("-id")
        supplier_ledgers = Supplier_ledger.objects.filter(author__user__username=request.user.username).order_by("-id")
        suppliers = Supplier.objects.filter(author__user__username=request.user.username).order_by("-id")
        
    products = helpers.pg_records(request, products, 5)
    supplier_ledgers = helpers.pg_records(request, supplier_ledgers, 5)
    suppliers = helpers.pg_records(request, suppliers, 5)

    return render(request, 'cadmin/product_view.html', {'products': products, 'supplier_ledgers': supplier_ledgers, 'suppliers': suppliers, 'stock_amount': stock_amount, 'total_brands': total_brands})


@login_required
def product_list(request):
    if request.user.is_superuser:
        products = Product.objects.order_by("-id").all()
        purchases = Purchase.objects.order_by("-id").all()
        
        # for product in products:
        #     Product.objects.create(fix_value=product.fix_value, id= product.id, salePrice=product.salePrice, barcode=(product.fix_value+str(product.id)+str(int(product.salePrice))))
        # # product.barcode = product.fix_value + product.salePrice + product.id 
        query = request.GET.get("q")
        if query:
            products = products.filter(
                Q(id__icontains=query) |
                # Q(name__icontains=query) |
                # Q(description__icontains=query) |
                # Q(fix_value__icontains=query) |
                Q(barcode__icontains=query) 
                # Q(colour__icontains=query) |
                # Q(cost__icontains=query) |
                # Q(salePrice__icontains=query) |
                # Q(quantity__icontains=query) |
                # Q(bill__icontains=query) |
                # Q(created_at__icontains=query)  
                ).distinct()

    else:
        products = Product.objects.filter(author__user__username=request.user.username).order_by("-id")
        purchases = Purchase.objects.filter(author__user__username=request.user.username).order_by("-id")

    products = helpers.pg_records(request, products, 5)
    purchases = helpers.pg_records(request, purchases, 5)

    return render(request, 'cadmin/product_list.html', {'products': products, 'purchases': purchases})

@login_required
def product_add(request):
    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = ProductForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                new_product = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_product.author = author
                new_product.save()
                f.save_m2m()

            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                new_product = f.save()

            # if user is not a superuser
            else:
                new_product = f.save(commit=False)
                # new_product.author = Author.objects.get(user__username=request.user.username)
                new_product.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Products added.')
            return redirect('product_add')

    # if request is GET the show unbound form to the user
    else:
        f = ProductForm()
    return render(request, 'cadmin/product_add.html', {'form': f})



@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = ProductForm(request.POST, instance=product)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_product = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_product.author = author
                updated_product.save()
                f.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_product = f.save()
            # if user is not a superuser
            else:
                updated_product = f.save(commit=False)
                # updated_product.author = Author.objects.get(user__username=request.user.username)
                updated_product.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Product updated.')
            return redirect(reverse('product_update', args=[product.id]))

    # if request is GET the show unbound form to the user, along with data
    else:
        f = ProductForm(instance=product)

    return render(request, 'cadmin/product_update.html', {'form': f, 'product': product})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Product deleted')
    return redirect(next_page) 

# @login_required
# def purchase_product_add(request):
#     products = Product.objects.order_by("-id").all()
#     # If request is POST, create a bound form(form with data)
#     if request.method == "POST":
#         f = ProductForm(request.POST)

#         # check whether form is valid or not
#         # if the form is valid, save the data to the database
#         # and redirect the user back to the add post form

#         # If form is invalid show form with errors again
#         if f.is_valid():
#             # if author is not selected and user is superuser, then assign the post to the author named staff
#             if request.POST.get('author') == "" and request.user.is_superuser:
#                 new_product = f.save(commit=False)
#                 author = Author.objects.get(user__username='staff')
#                 new_product.author = author
#                 new_product.save()
#                 f.save_m2m()

#             # if author is selected and user is superuser
#             elif request.POST.get('author') and request.user.is_superuser:
#                 new_product = f.save()

#             # if user is not a superuser
#             else:
#                 new_product = f.save(commit=False)
#                 # new_product.author = Author.objects.get(user__username=request.user.username)
#                 new_product.save()
#                 f.save_m2m()

#             # messages.add_message(request, messages.INFO, 'Products added.')
#             # return redirect('purchase_product_add')

#     # if request is GET the show unbound form to the user
#     else:
#         f = ProductForm()

#     return render(request, 'cadmin/purchase_product_add.html', {'form': f, 'products': products})

# @login_required
# def purchase_product_list(request, supplier):
#     # produc = Product.objects.filter(supplier=supplier).first()
#     # If request is POST, create a bound form(form with data)
#     if request.user.is_superuser:
#         if supplier: 
#             product = Product.objects.filter(supplier=supplier).first()

#             if request.method == "POST":
#                 f = ProductForm(request.POST)

#                 # check whether form is valid or not
#                 # if the form is valid, save the data to the database
#                 # and redirect the user back to the add post form

#                 # If form is invalid show form with errors again
#                 if f.is_valid():
#                     # if author is not selected and user is superuser, then assign the post to the author named staff
#                     if request.POST.get('author') == "" and request.user.is_superuser:
#                         new_product = f.save(commit=False)
#                         author = Author.objects.get(user__username='staff')
#                         new_product.author = author
#                         new_product.save()
#                         f.save_m2m()

#                     # if author is selected and user is superuser
#                     elif request.POST.get('author') and request.user.is_superuser:
#                         new_product = f.save()

#                     # if user is not a superuser
#                     else:
#                         new_product = f.save(commit=False)
#                         # new_product.author = Author.objects.get(user__username=request.user.username)
#                         new_product.save()
#                         f.save_m2m()

#                     messages.add_message(request, messages.INFO, 'Products added.')
#                     # return redirect('purchase_product_list', args=[product.id])
#                 return redirect(reverse('purchase_product_list', args=[product.supplier.id]))

#             # if request is GET the show unbound form to the user
#             else:
#                 f = ProductForm()

#             products = Product.objects.order_by("-id").all()
#             suppliers = Supplier.objects.order_by("-id").all()
#             supplier_ledgers = Supplier_Ledger.objects.order_by("-id").all()
#             total_bill = 0
#             total_amountPaid = 0
#             total_balacnce = 0
#             total_supplier = 0
#             supplier_id = product.supplier.id
#             for product in products:
#                 if supplier_id == product.supplier.id:
#                     for supplier in suppliers:
#                         if product.supplier.id == supplier.id:
#                             product.supplier.id  == supplier.id
#                             total_supplier = total_supplier + 1  
#                             total_bill = total_bill + product.bill
#                     for supplier_ledger in supplier_ledgers:
#                         if product.supplier.id == supplier_ledger.supplier.id: 
#                             total_amountPaid = total_amountPaid + supplier_ledger.amount_paid
#                             total_balance = total_bill - total_amountPaid

#     else:
#         products = Product.objects.filter(author__user__username=request.user.username).order_by("-id")
#         suppliers = Supplier.objects.filter(author__user__username=request.user.username).order_by("-id")
#         supplier_ledgers = Supplier_Ledger.objects.filter(author__user__username=request.user.username).order_by("-id")

#     products = helpers.pg_records(request, products, 5)
#     suppliers = helpers.pg_records(request, suppliers, 5)
#     supplier_ledgers = helpers.pg_records(request, supplier_ledgers, 5)

#     return render(request, 'cadmin/purchase_product_list.html', {'form': f, 'product': product, 'total_supplier': total_supplier,'supplier_id': supplier_id, 'products': products, 'suppliers': suppliers, 'supplier_ledgers': supplier_ledgers, 'total_bill': total_bill, 'total_amountPaid': total_amountPaid, 'total_balance': total_balance})


@login_required
def customer_view(request, pk=None):
    if request.user.is_superuser:
        if pk:
            customer = Customer.objects.get(pk=pk)
            customers = Customer.objects.order_by("-id").all()
            sales = Sale.objects.order_by("-id").all()
            customer_ledgers = Customer_Ledger.objects.order_by("-id").all()
            products = Product.objects.order_by("-id").all()
            sale_products = Sale_Product.objects.order_by("-id").all()

            total_business = 0
            total_balance = 0
            total_payment = 0
            total_amountReceived = 0
            customer_id=customer.id
            for sale in sales:
                for customer in customers:
                    for sale_product in sale_products:
                        if customer_id == customer.id:
                            if customer.id == sale.customer.id: 
                                if sale_product.sale.id == sale.id:                    
                                    total_business = total_business + sale.totalBill
                                    total_payment = total_payment + sale.totalBill
                                    total_balance = (-(sale.totalBill-sale.discount)+sale.receivedAmount)
                                    total_amountReceived = sale.receivedAmount 

                                    # for customer_ledger in customer_ledgers: 
                                    #     if sale.customer.id == customer_ledger.customer.id:
                                    #         total_balance = total_balance + (-(product.bill-sale.discount)+customer_ledger.amount_received)
                                    #         total_amountReceived = customer_ledger.amount_received 
                                        

    return render(request, 'cadmin/customer_view.html', {'customers': customers, 'customer_id': customer_id, 'sales': sales, 'customer_ledgers': customer_ledgers, 'products': products, 'sale_products': sale_products, 'total_business':total_business, 'total_balance':total_balance, 'total_amountReceived':total_amountReceived, 'total_payment':total_payment})

@login_required
def customer_list(request):
    if request.user.is_superuser:
        customers = Customer.objects.order_by("-id").all()
        invoices = Invoice.objects.order_by("-id").all()
        query = request.GET.get("q")
        if query:
            customers = customers.filter(
                Q(id__icontains=query) 
                # Q(name__icontains=query) |
                # Q(contact__icontains=query) |
                # Q(email__icontains=query) |
                # Q(address__icontains=query) |
                # Q(created_at__icontains=query)   
                ).distinct()
    else:
        customers = Customer.objects.filter(author__user__username=request.user.username).order_by("-id")
        invoices = Invoice.objects.filter(author__user__username=request.user.username).order_by("-id")

    customers = helpers.pg_records(request, customers, 5)
    invoices = helpers.pg_records(request, invoices, 5)

    return render(request, 'cadmin/customer_list.html', {'customers': customers, 'invoices': invoices})

@login_required
def customer_add(request):
    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = CustomerForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                new_customer = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_customer.author = author
                new_customer.save()
                f.save_m2m()

            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                new_customer = f.save()

            # if user is not a superuser
            else:
                new_customer = f.save(commit=False)
                # new_customer.author = Author.objects.get(user__username=request.user.username)
                new_customer.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Customer added.')
            return redirect('sale_add')

    # if request is GET the show unbound form to the user
    else:
        f = CustomerForm()
    return render(request, 'cadmin/customer_add.html', {'form': f})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = CustomerForm(request.POST, instance=customer)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_customer = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_customer.author = author
                updated_customer.save()
                f.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_customer = f.save()
            # if user is not a superuser
            else:
                updated_customer = f.save(commit=False)
                # updated_customer.author = Author.objects.get(user__username=request.user.username)
                updated_customer.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Customer updated.')
            return redirect(reverse('sale_add'))

    # if request is GET the show unbound form to the user, along with data
    else:
        f = CustomerForm(instance=customer)

    return render(request, 'cadmin/customer_update.html', {'form': f, 'customer': customer})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Customer deleted')
    return redirect(next_page)                       


@login_required
def sale_list(request):
    if request.user.is_superuser:
        sales = Sale.objects.order_by("-id").all()
        products = Product.objects.order_by("-id").all()
        customer_ledgers = Customer_Ledger.objects.order_by("-id").all()

        query = request.GET.get("q")
        if query:
            sales = sales.filter(
                Q(id__icontains=query) 
                # Q(customer__icontains=query) |
                # Q(product__icontains=query) |
                # Q(totalBill__icontains=query) |
                # Q(discount__icontains=query) |
                # Q(receivedAmount__icontains=query) |
                # Q(balance__icontains=query) |
                # Q(created_at__icontains=query)  
                ).distinct() 
    else:
        sales = Sale.objects.filter(author__user__username=request.user.username).order_by("-id")
        products = Product.objects.filter(author__user__username=request.user.username).order_by("-id")
        customer_ledgers = Customer_Ledger.objects.filter(author__user__username=request.user.username).order_by("-id")

    sales = helpers.pg_records(request, sales, 5)
    products = helpers.pg_records(request, products, 5)
    customer_ledgers = helpers.pg_records(request, customer_ledgers, 5)

    return render(request, 'cadmin/sale_list.html', {'sales': sales, 'products': products, 'customer_ledgers' : customer_ledgers})

@login_required
def sale_add(request):

    if 'search_text' in request.session:
        search_text = request.session['search_text']
    #     print(search_text)
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    products = Product.objects.order_by("-id").all()
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False
    SaleProductFormSet = formset_factory(SaleProductForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST': # If the form has been submitted...
        sale_form = SaleForm(request.POST) # A form bound to the POST data
        # print(sale_form)
        # Create a formset from the submitted data
        sale_product_formset = SaleProductFormSet(request.POST, request.FILES)
        # print(sale_product_formset)

        if sale_form.is_valid() and sale_product_formset.is_valid():
            print(sale_form)
            sale = sale_form.save()
            for form in sale_product_formset.forms:
                print(sale_product_formset)
                sale_product = form.save(commit=False)
                sale_product.sale = sale
                # sale_product.product = product
                sale_product.save()
            return redirect('sale_list') # Redirect to a 'success' page
    else:
        sale_form = SaleForm()
        sale_product_formset = SaleProductFormSet()

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'sale_form': sale_form,
         'sale_product_formset': sale_product_formset,
         'products' : products,
         'search_text': search_text,
        }
    c.update(csrf(request))

    return render_to_response('cadmin/sale_add.html', c)

@login_required
def search(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
        request.session['search_text'] = search_text
        # print(search_text)
    else:
        search_text = ''    
    products = Product.objects.filter(barcode__contains=search_text)
    return render_to_response('cadmin/ajax_search.html', {'products': products, 'search_text': search_text})    

@login_required
def sale_add1(request):
    # a = search(request)
    if 'search_text' in request.session:
        search_text = request.session['search_text']
        # print(search_text)
    products = Product.objects.order_by("-id").all()
    
    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = SaleForm(request.POST)
        print(f)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            
            new_sale = f.save(commit=False)
            # new_customer.author = Author.objects.get(user__username=request.user.username)
            new_sale.save()
            f.save_m2m()
            messages.add_message(request, messages.INFO, 'Sale added.')
            return redirect('sale_add1')

    # if request is GET the show unbound form to the user
    else:
        f = SaleForm()
    return render(request, 'cadmin/sale_add1.html', {'form': f, 'products' : products, 'search_text': search_text})    

@login_required
def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = SaleForm(request.POST, instance=sale)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_sale = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_sale.author = author
                updated_sale.save()
                f.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_sale = f.save()
            # if user is not a superuser
            else:
                updated_sale = f.save(commit=False)
                # updated_sale.author = Author.objects.get(user__username=request.user.username)
                updated_sale.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Sale updated.')
            return redirect(reverse('sale_update', args=[sale.id]))

    # if request is GET the show unbound form to the user, along with data
    else:
        f = SaleForm(instance=sale)

    return render(request, 'cadmin/sale_update.html', {'form': f, 'sale': sale})

@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    sale.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Sale deleted')
    return redirect(next_page)  

@login_required
def customer_ledger_list(request):
    if request.user.is_superuser:
        customer_ledgers = Customer_Ledger.objects.order_by("-id").all()
        query = request.GET.get("q")
        if query:
            customer_ledgers = customer_ledgers.filter(
                Q(id__icontains=query)
                # Q(customer__icontains=query) |
                # Q(amount_received__icontains=query) |
                # Q(created_at__icontains=query) 
                ).distinct()
    else:
        customer_ledgers = Customer_Ledger.objects.filter(author__user__username=request.user.username).order_by("-id")

    customer_ledgers = helpers.pg_records(request, customer_ledgers, 5)

    return render(request, 'cadmin/customer_ledger_list.html', {'customer_ledgers': customer_ledgers})

@login_required
def customer_ledger_add(request):
    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = CustomerLedgerForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                new_customer_ledger = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_customer_ledger.author = author
                new_customer_ledger.save()
                f.save_m2m()

            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                new_customer_ledger = f.save()

            # if user is not a superuser
            else:
                new_customer_ledger = f.save(commit=False)
                # new_customer_ledger.author = Author.objects.get(user__username=request.user.username)
                new_customer_ledger.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Customer Ledger added.')
            return redirect('customer_ledger_list')

    # if request is GET the show unbound form to the user
    else:
        f = CustomerLedgerForm()
    return render(request, 'cadmin/customer_ledger_add.html', {'form': f})

@login_required
def customer_ledger_update(request, pk):
    customer_ledger = get_object_or_404(Customer_Ledger, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = CustomerLedgerForm(request.POST, instance=customer_ledger)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_customer_ledger = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_customer_ledger.author = author
                updated_customer_ledger.save()
                f.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_customer_ledger = f.save()
            # if user is not a superuser
            else:
                updated_customer_ledger = f.save(commit=False)
                # updated_customer_ledger.author = Author.objects.get(user__username=request.user.username)
                updated_customer_ledger.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Customer Ledger updated.')
            return redirect(reverse('customer_ledger_list', args=[customer_ledger.id]))

    # if request is GET the show unbound form to the user, along with data
    else:
        f = CustomerLedgerForm(instance=customer_ledger)

    return render(request, 'cadmin/customer_ledger_update.html', {'form': f, 'customer_ledger': customer_ledger})

@login_required
def customer_ledger_delete(request, pk):
    customer_ledger = get_object_or_404(Customer_Ledger, pk=pk)
    customer_ledger.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Customer Ledger deleted')
    return redirect(next_page)    


# def subtract(value, arg):
#     return value - arg


@login_required
def purchase_view(request):
    if request.user.is_superuser:
        purchases = Purchase.objects.order_by("-id").all()
        products = Product.objects.order_by("-id").all()
        supplier_ledgers = Supplier_Ledger.objects.order_by("-id").all()
        total_quantity = 0
        stock_amount = 0
        for product in products:
            total_quantity = total_quantity + product.quantity
        
        for supplier_ledger in supplier_ledgers:
            stock_amount = stock_amount + supplier_ledger.amount_paid    

    else:
        purchases = Purchase.objects.filter(author__user__username=request.user.username).order_by("-id")
        products = Product.objects.filter(author__user__username=request.user.username).order_by("-id")
        supplier_ledgers = Supplier_Ledger.objects.filter(author__user__username=request.user.username).order_by("-id")
   
    purchases = helpers.pg_records(request, purchases, 5)
    products = helpers.pg_records(request, products, 5)
    supplier_ledgers = helpers.pg_records(request, supplier_ledgers, 5)

    return render(request, 'cadmin/purchase_view.html', {'purchases': purchases,'products': products, 'supplier_ledgers' : supplier_ledgers, 'total_quantity': total_quantity, 'stock_amount': stock_amount})

@login_required
def sale_view(request):
    if request.user.is_superuser:
        sales = Sale.objects.order_by("-id").all()
        products = Product.objects.order_by("-id").all()
        customer_ledgers = Customer_Ledger.objects.order_by("-id").all()
        total_quantity = 0
        stock_amount = 0
        for product in products:
            total_quantity = total_quantity + product.quantity
        
        for customer_ledger in customer_ledgers:
            stock_amount = stock_amount + customer_ledger.amount_received    

    else:
        sales = Sale.objects.filter(author__user__username=request.user.username).order_by("-id")
        products = Product.objects.filter(author__user__username=request.user.username).order_by("-id")
        customer_ledgers = Supplier_Ledger.objects.filter(author__user__username=request.user.username).order_by("-id")
   
    sales = helpers.pg_records(request, sales, 5)
    products = helpers.pg_records(request, products, 5)
    customer_ledgers = helpers.pg_records(request, customer_ledgers, 5)

    return render(request, 'cadmin/sale_view.html', {'sales': sales,'products': products, 'customer_ledgers' : customer_ledgers, 'total_quantity': total_quantity, 'stock_amount': stock_amount})







# # total_bill = 0
# # total_amountPaid = 0
# # total_balance = 0
# # total_supplier = 0
# @login_required
# def purchase_product_add(request):
#     id_product_global = 0
#     temp_id = 0
#     temp_name = ""
#     temp_description = ""
#     temp_barcode = ""
#     temp_brand = ""
#     temp_colour = ""
#     temp_cost = 0.0
#     temp_salePrice = 0.0
#     temp_quantity = 0
#     temp_bill = 0.0
#     count = 0
#     products = Product.objects.order_by("-id").all()
#     # If request is POST, create a bound form(form with data)
#     if request.method == "POST":
#         f = ProductForm(request.POST)

#         # check whether form is valid or not
#         # if the form is valid, save the data to the database
#         # and redirect the user back to the add post form

#         # If form is invalid show form with errors again
#         if f.is_valid():
#             # if author is not selected and user is superuser, then assign the post to the author named staff
#             # if request.POST.get('author') == "" and request.user.is_superuser:
#             #     new_product = f.save(commit=False)
#             #     author = Author.objects.get(user__username='staff')
#             #     new_product.author = author
#             #     new_product.save()
#             #     f.save_m2m()
#             #     id_product_global = new_product.id
#             #     print('after save in db cookie:' + new_product.id)

#             # # if author is selected and user is superuser
#             # elif request.POST.get('author') and request.user.is_superuser:
#             #     new_product = f.save()
#             #     id_product_global = new_product.id
#             #     print('after save in db cookie:' + new_product.id)
#             # if user is not a superuser
#             # else:
            

#             new_product = f.save(commit=False)
#             # new_product.author = Author.objects.get(user__username=request.user.username)
#             new_product.save()
#             for product in products:
#                 if count == 0:
#                     temp_id = product.id
#                     temp_name = product.name
#                     temp_description = product.description
#                     temp_barcode = product.barcode_generated
#                     temp_brand = product.brand
#                     temp_colour = product.colour
#                     temp_cost = product.cost
#                     temp_salePrice = product.salePrice
#                     temp_quantity = product.quantity
#                     temp_bill = product.bill
#                     count = 2
#                 # for product in products:
#                     # new_product.temp_id
#                     # new_product.temp_name
#                     # new_product.temp_description
#                     # new_product.temp_brand 
#                     # new_product.temp_colour
#                     # new_product.temp_cost 
#                     # new_product.temp_salePrice
#                     # new_product.temp_quantity 
#             f.save_m2m()
#             id_product_global = new_product.id
#             print('after save in db cookie:' + str(new_product.id))

#             messages.add_message(request, messages.INFO, 'Products added.')
                
#             f= ProductForm()

#             # f = ProductForm()

#     # if request is GET the show unbound form to the user
#     else:
#         f = ProductForm()

#     if request.user.is_superuser:
#         suppliers = Supplier.objects.order_by("-id").all()
#         supplier_ledgers = Supplier_Ledger.objects.order_by("-id").all()
#         total_bill = 0
#         total_amountPaid = 0
#         total_balance = 0
#         count = 0
#         total_supplier = 0
#         p_id = request.COOKIES.get('list_ids')
#         print(p_id)
#         if(p_id):
#             idList = [int(e) if e.isdigit() else e for e in p_id.split(',')]
#             print(idList)
#             listId2 = []
#             for n in idList:
#                 if(n != 0 and n!= 'None' ):
#                     listId2.append(n)
#             print(listId2)
#             products = Product.objects.order_by("-id").filter(id__in = listId2)
#             # suppliers = Supplier.objects.order_by("-id").all()
#             # supplier_ledgers = Supplier_Ledger.objects.order_by("-id").all()
#             # total_bill = 0
#             # total_amountPaid = 0
#             # total_balance = 0
#             # total_supplier = 0
#             # supplier_id = product.supplier.id
#             for product in products:
#                 # if supplier_id == product.supplier.id:
#                 for supplier in suppliers:
#                     if product.supplier.id == supplier.id:
#                         # if count == 0:
#                         request.session['supplier.id'] = supplier.id
#                         print(supplier.id)
#                             # count = 1
            
#                         total_supplier = total_supplier + 1
#                         total_bill = total_bill + product.bill
                
#                         request.session['total_supplier'] = total_supplier
#                         request.session['total_bill'] = int(total_bill)
                            
#                     for supplier_ledger in supplier_ledgers:
#                         if product.supplier.id == supplier_ledger.supplier.id:
#                             if count == 0:
#                                 total_amountPaid = supplier_ledger.amount_paid
#                                 total_balance = total_bill - total_amountPaid
#                                 request.session['total_amountPaid'] = int(total_amountPaid)
#                                 request.session['total_balance'] = int(total_balance)
#                                 count = 3 

#     else:
#         products = Product.objects.filter(author__user__username=request.user.username).order_by("-id")
#         suppliers = Supplier.objects.filter(author__user__username=request.user.username).order_by("-id")
#         supplier_ledgers = Supplier_Ledger.objects.filter(author__user__username=request.user.username).order_by("-id")

#     products = helpers.pg_records(request, products, 5)
#     suppliers = helpers.pg_records(request, suppliers, 5)
#     supplier_ledgers = helpers.pg_records(request, supplier_ledgers, 5)
            
#     response = render(request, 'cadmin/purchase_product_add.html', {'form': f, 'temp_id': temp_id, 'temp_name': temp_name, 'temp_description': temp_description, 'temp_barcode': temp_barcode, 'temp_brand': temp_brand, 'temp_colour': temp_colour, 'temp_cost': temp_cost, 'temp_salePrice': temp_salePrice, 'temp_quantity': temp_quantity, 'temp_bill': temp_bill, 'total_supplier': total_supplier, 'products': products, 'suppliers': suppliers, 'supplier_ledgers': supplier_ledgers, 'total_bill': total_bill, 'total_amountPaid': total_amountPaid, 'total_balance': total_balance})
#     print('on set cookie:' + str(id_product_global)) 
#     p_id = request.COOKIES.get('list_ids')
#     if(len(str(p_id)) != 0 and str(p_id) != 'None'):
#         p_id = str(p_id)+','+str(id_product_global)
#     else:
#         p_id= str(id_product_global)
#     response.set_cookie(key='list_ids', value= p_id)

#     # response.set_cookie(key='total_supplier', value= total_supplier)
#     # response.set_cookie(key='total_bill', value= total_bill)
#     # response.set_cookie(key='total_amountPaid', value= total_amountPaid)
#     # response.set_cookie(key='total_balance', value= total_balance)
#     return response