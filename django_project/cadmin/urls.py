from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^activate/account/$', views.activate_account, name='activate'),
    url(r'^register/$', views.register, name='register'),
    url(r'^password-change-done/$',
        auth_views.password_change_done,
        {'template_name': 'cadmin/password_change_done.html'},
        name='password_change_done'
        ),
    url(r'^password-change/$',
        auth_views.password_change,
        {'template_name': 'cadmin/password_change.html' , 'post_change_redirect': 'password_change_done'},
        name='password_change'
        ),
    url(r'^login/$', views.login, {'template_name': 'cadmin/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'cadmin/logout.html'}, name='logout'),
    url(r'^account-info/$', views.account_info, name='account_info'),

#----------------------------------------------------------------------------#
# If i remove these two views it gives me error what's wrong with these views
    url(r'^category/$', views.category_list, name='category_list'),
    url(r'^tag/$', views.tag_list, name='tag_list'),
# See them later  
#------------------------------------------------------------------------------#  
    url(r'^$', views.index, name='index'),
    url(r'^barcode/$', views.barcode, name='barcode'),
    url(r'^invoice/show/(?P<pk>[\d]+)/$', views.invoice_show, name='invoice_show'),
    url(r'^supplier/$', views.supplier_list, name='supplier_list'),
    url(r'^supplier/add/$', views.supplier_add, name='supplier_add'),
    url(r'^supplier/view/(?P<pk>[\d]+)/$', views.supplier_view, name='supplier_view'),
    url(r'^supplier/update/(?P<pk>[\d]+)/$', views.supplier_update, name='supplier_update'),
    url(r'^supplier/delete/(?P<pk>[\d]+)/$', views.supplier_delete, name='supplier_delete'),

    url(r'^supplier_ledger/$', views.supplier_ledger_list, name='supplier_ledger_list'),
    url(r'^supplier_ledger/add/$', views.supplier_ledger_add, name='supplier_ledger_add'),
    url(r'^supplier_ledger/update/(?P<pk>[\d]+)/$', views.supplier_ledger_update, name='supplier_ledger_update'),
    url(r'^supplier_ledger/delete/(?P<pk>[\d]+)/$', views.supplier_ledger_delete, name='supplier_ledger_delete'),

    url(r'^product/$', views.product_list, name='product_list'),
    url(r'^product/add/$', views.product_add, name='product_add'),
    # url(r'^purchase/product/add/$', views.purchase_product_add, name='purchase_product_add'),
    # url(r'^purchase/product/add/(?P<supplier>[\d]+)/$', views.purchase_product_add, name='purchase_product_add'),
    # url(r'^purchase/product/list/(?P<supplier>[\d]+)/$', views.purchase_product_list, name='purchase_product_list'),
    url(r'^product/view/$', views.product_view, name='product_view'),
    url(r'^product/update/(?P<pk>[\d]+)/$', views.product_update, name='product_update'),
    url(r'^product/delete/(?P<pk>[\d]+)/$', views.product_delete, name='product_delete'),

    url(r'^purchase/$', views.purchase_list, name='purchase_list'),
    url(r'^purchase/add/$', views.purchase_add, name='purchase_add'),
    url(r'^purchase/view/$', views.purchase_view, name='purchase_view'),
    url(r'^purchase/update/(?P<pk>[\d]+)/$', views.purchase_update, name='purchase_update'),
    url(r'^purchase/delete/(?P<pk>[\d]+)/$', views.purchase_delete, name='purchase_delete'),

    url(r'^customer/$', views.customer_list, name='customer_list'),
    url(r'^customer/add/$', views.customer_add, name='customer_add'),
    url(r'^customer/view/(?P<pk>[\d]+)/$', views.customer_view, name='customer_view'),
    url(r'^customer/update/(?P<pk>[\d]+)/$', views.customer_update, name='customer_update'),
    url(r'^customer/delete/(?P<pk>[\d]+)/$', views.customer_delete, name='customer_delete'),

    url(r'^sale/$', views.sale_list, name='sale_list'),
    url(r'^sale/add/$', views.sale_add, name='sale_add'),
    url(r'^sale/add1/$', views.sale_add1, name='sale_add1'),
    url(r'^search/$', views.search, name='search'),
    url(r'^sale/view/$', views.sale_view, name='sale_view'),
    url(r'^sale/update/(?P<pk>[\d]+)/$', views.sale_update, name='sale_update'),
    url(r'^sale/delete/(?P<pk>[\d]+)/$', views.sale_delete, name='sale_delete'),

    url(r'^customer_ledger/$', views.customer_ledger_list, name='customer_ledger_list'),
    url(r'^customer_ledger/add/$', views.customer_ledger_add, name='customer_ledger_add'),
    url(r'^customer_ledger/update/(?P<pk>[\d]+)/$', views.customer_ledger_update, name='customer_ledger_update'),
    url(r'^customer_ledger/delete/(?P<pk>[\d]+)/$', views.customer_ledger_delete, name='customer_ledger_delete'),
]