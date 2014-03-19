# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Sales module views
"""
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from treeio.sales.models import Product, SaleOrder, SaleSource, Lead, Opportunity, \
    SaleStatus, Subscription, OrderedProduct
from treeio.sales.forms import SettingsForm, OrderForm, ProductForm, SaleStatusForm, UpdateRecordForm, \
    LeadForm, OpportunityForm, OrderedProductForm, SubscriptionForm, \
    OrderFilterForm, LeadFilterForm, OpportunityFilterForm, ProductFilterForm, \
    MassActionForm, ProductMassActionForm, LeadMassActionForm, \
    OpportunityMassActionForm, SaleSourceForm
from treeio.core.rendering import render_to_response
from treeio.core.models import Object, ModuleSetting, UpdateRecord
from treeio.core.views import user_denied
from treeio.core.decorators import treeio_login_required, handle_response_format, module_admin_required
from treeio.identities.models import Contact
from treeio.finance.models import Currency
from treeio.finance.helpers import convert


def _get_filter_query(args, model=SaleOrder):
    "Compose a filter query based on filter form submission"
    query = Q()

    for arg in args:
        if args[arg]:
            if hasattr(model, arg) or arg == 'products_interested':
                kwargs = {str(arg + '__id'): long(args[arg])}
                query = query & Q(**kwargs)

    return query


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Orders"

    def wrap(request, *args, **kwargs):
        "Wrap"
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-order' in key:
                    try:
                        order = SaleOrder.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            request.user.get_profile(), request.POST, instance=order)
                        if form.is_valid() and request.user.get_profile().has_permission(order, mode='w'):
                            form.save()
                    except:
                        pass

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


def _process_mass_lead_form(f):
    "Pre-process request to handle mass action form for Orders"

    def wrap(request, *args, **kwargs):
        "Wrap"
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-lead' in key:
                    try:
                        lead = Lead.objects.get(pk=request.POST[key])
                        form = LeadMassActionForm(
                            request.user.get_profile(), request.POST, instance=lead)
                        if form.is_valid() and request.user.get_profile().has_permission(lead, mode='w'):
                            form.save()
                    except:
                        pass

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


def _process_mass_opportunity_form(f):
    "Pre-process request to handle mass action form for Orders"

    def wrap(request, *args, **kwargs):
        "Wrap"
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-opportunity' in key:
                    try:
                        opportunity = Opportunity.objects.get(
                            pk=request.POST[key])
                        form = OpportunityMassActionForm(request.user.get_profile(),
                                                         request.POST, instance=opportunity)
                        if form.is_valid() and request.user.get_profile().has_permission(opportunity,
                                                                                         mode='w'):
                            form.save()
                    except:
                        pass

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


def _do_update_record(profile, request, object):
    "Get the Update Record Form"
    if profile.has_permission(object, mode='x'):
        if request.POST:
            record = UpdateRecord()
            record.object = object
            record.record_type = 'manual'
            form = UpdateRecordForm(request.POST, instance=record)
            if form.is_valid():
                record = form.save()
                record.set_user_from_request(request)
                record.save()
                record.about.add(object)
                object.set_last_updated()
        else:
            form = UpdateRecordForm()
    else:
        form = None
    return form


@treeio_login_required
@handle_response_format
@_process_mass_form
def index(request, response_format='html'):
    "Sales index page"

    query = Q(status__hidden=False)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = query & _get_filter_query(request.GET)
    orders = Object.filter_by_request(
        request, SaleOrder.objects.filter(query), mode="r")
    filters = OrderFilterForm(request.user.get_profile(), '', request.GET)
    statuses = Object.filter_by_request(request, SaleStatus.objects, mode="r")

    massform = MassActionForm(request.user.get_profile())

    return render_to_response('sales/index',
                              {'orders': orders,
                               'filters': filters,
                               'statuses': statuses,
                               'massform': massform
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
@_process_mass_form
def index_assigned(request, response_format='html'):
    "Orders assigned to current user"

    query = Q(status__hidden=False, assigned=request.user.get_profile())
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = query & _get_filter_query(request.GET)

    orders = Object.filter_by_request(
        request, SaleOrder.objects.filter(query), mode="r")
    filters = OrderFilterForm(
        request.user.get_profile(), 'assigned', request.GET)
    statuses = Object.filter_by_request(request, SaleStatus.objects, mode="r")

    massform = MassActionForm(request.user.get_profile())

    return render_to_response('sales/index_assigned',
                              {'orders': orders,
                               'statuses': statuses,
                               'massform': massform,
                               'filters': filters},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def index_status(request, response_format='html'):
    "Index Status"
    query = Q(status__hidden=False)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = query & _get_filter_query(request.GET)

    orders = Object.filter_by_request(
        request, SaleOrder.objects.filter(query), mode="r")
    statuses = Object.filter_by_request(request, SaleStatus.objects, mode="r")
    filters = OrderFilterForm(request.user.get_profile(), '', request.GET)

    total = 0

    for status in statuses:
        status.count = 0
        for order in orders:
            if order.status == status:
                if order.status.hidden is False:
                    total += 1
                    status.count += order.quantity

    return render_to_response('sales/index_status',
                              {'orders': orders,
                               'statuses': statuses,
                               'total': total,
                               'filters': filters
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_open(request, response_format='html'):
    "SaleOrders owned by current user"
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.sales', 'order_fulfil_status')[0]
        fulfil_status = long(conf.value)
        query = Q(status__hidden=False) & ~Q(status=fulfil_status)
    except Exception:
        query = Q(status__hidden=False)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET) & Q(user=request.user)
        else:
            query = query & _get_filter_query(request.GET)

    orders = Object.filter_by_request(
        request, SaleOrder.objects.filter(query), mode="r")
    statuses = Object.filter_by_request(request, SaleStatus.objects)
    filters = OrderFilterForm(request.user.get_profile(), '', request.GET)

    massform = MassActionForm(request.user.get_profile())

    return render_to_response('sales/index_open',
                              {'orders': orders,
                               'statuses': statuses,
                               'massform': massform,
                               'filters': filters},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def ordered_product_add(request, order_id=None, response_format='html'):
    "Add new Ordered Product"

    order = get_object_or_404(SaleOrder, pk=order_id)
    if not request.user.get_profile().has_permission(order, mode='x'):
        return user_denied("Sorry, you don't have access to this Sale Order")

    if request.POST:
        if not 'cancel' in request.POST:
            ordered_product = OrderedProduct()
            ordered_product.order = order
            form = OrderedProductForm(
                request.user.get_profile(), order, request.POST, instance=ordered_product)
            if form.is_valid():
                ordered_product = form.save(commit=False)
                convert(
                    ordered_product, 'rate', currency=ordered_product.order.currency)
                ordered_product.set_user_from_request(request)
                ordered_product.order.update_total()
                if 'add_another' in request.POST:
                    return HttpResponseRedirect(reverse('sales_ordered_product_add', args=[order.id]))
                return HttpResponseRedirect(reverse('sales_order_view', args=[order.id]))
        else:
            return HttpResponseRedirect(reverse('sales_order_view', args=[order.id]))
    else:
        form = OrderedProductForm(request.user.get_profile(), order)

    return render_to_response('sales/ordered_product_add',
                              {'form': form,
                               'order': order},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def ordered_product_view(request, ordered_product_id, response_format='html'):
    "Ordered product view"
    ordered_product = get_object_or_404(OrderedProduct, pk=ordered_product_id)
    if not request.user.get_profile().has_permission(ordered_product) \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, message="You don't have access to this Ordered Product")

    return render_to_response('sales/ordered_product_view',
                              {'ordered_product': ordered_product},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def ordered_product_edit(request, ordered_product_id, response_format='html'):
    "OrderedProduct edit"

    ordered_product = get_object_or_404(OrderedProduct, pk=ordered_product_id)
    if not request.user.get_profile().has_permission(ordered_product, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this OrderedProduct", response_format)

    order = ordered_product.order
    if request.POST:
        if not 'cancel' in request.POST:
            form = OrderedProductForm(
                request.user.get_profile(), order, request.POST, instance=ordered_product)
            if form.is_valid():
                ordered_product = form.save(commit=False)
                convert(
                    ordered_product, 'rate', currency=ordered_product.order.currency)
                ordered_product.order.update_total()
                return HttpResponseRedirect(reverse('sales_ordered_product_view', args=[ordered_product.id]))
        else:
            return HttpResponseRedirect(reverse('sales_ordered_product_view', args=[ordered_product.id]))
    else:
        form = OrderedProductForm(
            request.user.get_profile(), order, instance=ordered_product)

    return render_to_response('sales/ordered_product_edit',
                              {'form': form,
                               'ordered_product': ordered_product,
                               'order': order
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def ordered_product_delete(request, ordered_product_id, response_format='html'):
    "OrderedProduct delete"

    ordered_product = get_object_or_404(OrderedProduct, pk=ordered_product_id)
    if not request.user.get_profile().has_permission(ordered_product, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Sale Status", response_format)

    if request.POST:
        if 'delete' in request.POST:
            order_id = ordered_product.order_id
            if 'trash' in request.POST:
                ordered_product.trash = True
                ordered_product.save()
            else:
                ordered_product.delete()
            ordered_product.order.update_total()
            return HttpResponseRedirect(reverse('sales_order_view', args=[order_id]))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('sales_ordered_product_view', args=[ordered_product.id]))

    order = ordered_product.order

    return render_to_response('sales/ordered_product_delete',
                              {'ordered_product': ordered_product,
                               'order': order},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def subscription_index(request, response_format='html'):
    "Subscription index page"

    query = Q(status__hidden=False)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = query & _get_filter_query(request.GET)

    subscriptions = Object.filter_by_request(
        request, Subscription.objects.filter(query), mode="r")
    filters = OrderFilterForm(request.user.get_profile(), '', request.GET)
    ordered_products = subscriptions.orderedproduct_set.all()
    orders = ordered_products.order_set.all()
    #orders = Object.filter_by_request(request, SaleOrder.objects, mode = "r")
    statuses = Object.filter_by_request(request, SaleStatus.objects, mode="r")

    return render_to_response('sales/index',
                              {'orders': orders,
                               'products': ordered_products,
                               'filters': filters,
                               'statuses': statuses
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def subscription_add(request, order_id=None, product_id=None, productset_id=None, response_format='html'):
    "Product add"
    if order_id:
        order = get_object_or_404(SaleOrder, pk=order_id)
    if product_id:
        product = get_object_or_404(OrderedProduct, pk=product_id)
    if productset_id:
        productset = get_object_or_404(Product, pk=productset_id)

    subscription = Subscription()
    if order_id:
        subscription.client = order.client
    if product_id:
        subscription.product = product.product
    if productset_id:
        subscription.product = productset

    if request.POST:
        if not 'cancel' in request.POST:
            form = SubscriptionForm(
                request.user.get_profile(), request.POST, instance=subscription)
            if form.is_valid():
                subscription = form.save(commit=False)
                subscription.renew()
                subscription.save()
                subscription.set_user_from_request(request)
                if product_id:
                    product.subscription = subscription
                    product.save()
                if order_id:
                    return HttpResponseRedirect(reverse('sales_order_view', args=[order_id]))
                else:
                    return HttpResponseRedirect(reverse('sales_subscription_view', args=[subscription.id]))
        else:
            return HttpResponseRedirect(reverse('sales_product_index'))
    else:
        form = SubscriptionForm(
            request.user.get_profile(), instance=subscription)

    return render_to_response('sales/subscription_add',
                              {'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def subscription_view(request, subscription_id, response_format='html'):
    "Subscription view"

    subscription = get_object_or_404(Subscription, pk=subscription_id)
    if not request.user.get_profile().has_permission(subscription):
        return user_denied(request, message="You don't have access to this Subscription")

    query = Q(subscription=subscription)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = query & _get_filter_query(request.GET)
        else:
            query = query & Q(
                status__hidden=False) & _get_filter_query(request.GET)
    else:
        query = query & Q(status__hidden=False)
    ops = subscription.orderedproduct_set.all()
    orders = []
    for op in ops:
        orders.append(op.order)

    return render_to_response('sales/subscription_view',
                              {'subscription': subscription,

                               'orders': orders},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def subscription_edit(request, subscription_id, response_format='html'):
    "Subscription edit"

    subscription = get_object_or_404(Subscription, pk=subscription_id)
    if not request.user.get_profile().has_permission(subscription, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Subscription", response_format)

    if request.POST:
        form = SubscriptionForm(
            request.user.get_profile(), request.POST, instance=subscription)
    else:
        form = SubscriptionForm(
            request.user.get_profile(), instance=subscription)
    if form.is_valid():
        subscription = form.save()
        return HttpResponseRedirect(reverse('sales_subscription_view', args=[subscription.id]))

    return render_to_response('sales/subscription_edit',
                              {'form': form,
                               'subscription': subscription,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def subscription_delete(request, subscription_id, response_format='html'):
    "Subscription delete"

    subscription = get_object_or_404(Subscription, pk=subscription_id)
    if not request.user.get_profile().has_permission(subscription, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Sale Status", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                subscription.trash = True
                subscription.save()
            else:
                subscription.delete()
            return HttpResponseRedirect(reverse('sales_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('sales_subscription_view', args=[subscription.id]))

    return render_to_response('sales/subscription_delete',
                              {'subscription': subscription,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def product_index(request, response_format='html'):
    "Product index page"

    query = Q(status__hidden=False)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = query & _get_filter_query(request.GET)

    if 'massform' in request.POST:
        for key in request.POST:
            if 'mass-product' in key:
                try:
                    product = Product.objects.get(pk=request.POST[key])
                    form = ProductMassActionForm(
                        request.user.get_profile(), request.POST, instance=product)
                    if form.is_valid() and request.user.get_profile().has_permission(product, mode='w'):
                        form.save()
                except:
                    pass

    massform = ProductMassActionForm(request.user.get_profile())

    query = Q(parent__isnull=True)
    if request.GET:
        query = query & _get_filter_query(request.GET, model=Product)

    statuses = Object.filter_by_request(request, SaleStatus.objects, mode="r")
    products = Object.filter_by_request(
        request, Product.objects.filter(query), mode="r")
    filters = ProductFilterForm(request.user.get_profile(), '', request.GET)

    return render_to_response('sales/product_index',
                              {'products': products,
                               'filters': filters,
                               'massform': massform,
                               'statuses': statuses
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
@module_admin_required('treeio.sales')
def product_add(request, parent_id=None, response_format='html'):
    "Product add"

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))

    if request.POST:
        if not 'cancel' in request.POST:
            product = Product()
            form = ProductForm(
                request.user.get_profile(), None, request.POST, instance=product)
            if form.is_valid():
                product = form.save()
                product.set_user_from_request(request)
                return HttpResponseRedirect(reverse('sales_product_view', args=[product.id]))
        else:
            return HttpResponseRedirect(reverse('sales_product_index'))
    else:
        form = ProductForm(request.user.get_profile(), parent_id)

    return render_to_response('sales/product_add',
                              {'form': form,
                               'products': all_products},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def product_edit(request, product_id, response_format='html'):
    "Product edit"

    product = get_object_or_404(Product, pk=product_id)
    if not request.user.get_profile().has_permission(product, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Product", response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = ProductForm(
                request.user.get_profile(), None, request.POST, instance=product)
            if form.is_valid():
                product = form.save()
                return HttpResponseRedirect(reverse('sales_product_view', args=[product.id]))
        else:
            return HttpResponseRedirect(reverse('sales_product_view', args=[product.id]))
    else:
        form = ProductForm(request.user.get_profile(), None, instance=product)

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))

    return render_to_response('sales/product_edit',
                              {'form': form,
                               'product': product,
                               'products': all_products},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def product_view(request, product_id, response_format='html'):
    "Product view"

    product = get_object_or_404(Product, pk=product_id)
    if not request.user.get_profile().has_permission(product) \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, message="You don't have access to this Product")

    query = Q(product=product)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = query & _get_filter_query(request.GET)
        else:
            query = query & Q(
                status__hidden=False) & _get_filter_query(request.GET)
    else:
        query = query & Q(status__hidden=False)

    subproducts = Object.filter_by_request(
        request, Product.objects.filter(parent=product))
    subscriptions = product.subscription_set.all()

    return render_to_response('sales/product_view',
                              {'product': product,
                               'subproducts': subproducts,
                               'subscriptions': subscriptions,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def product_delete(request, product_id, response_format='html'):
    "Product delete"

    product = get_object_or_404(Product, pk=product_id)
    if not request.user.get_profile().has_permission(product, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Sale Status", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                product.trash = True
                product.save()
            else:
                product.delete()
            return HttpResponseRedirect(reverse('sales_product_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('sales_product_view', args=[product.id]))

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))
    statuses = Object.filter_by_request(request, SaleStatus.objects, mode="r")
    subproducts = Object.filter_by_request(
        request, Product.objects.filter(parent=product))

    return render_to_response('sales/product_delete',
                              {'product': product,
                               'subproducts': subproducts,
                               'products': all_products,
                               'statuses': statuses},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
@_process_mass_lead_form
def lead_index(request, response_format='html'):
    "Lead index page"

    query = Q(status__hidden=False)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = query & _get_filter_query(request.GET)

    filters = LeadFilterForm(request.user.get_profile(), '', request.GET)

    statuses = Object.filter_by_request(request, SaleStatus.objects, mode="r")
    leads = Object.filter_by_request(
        request, Lead.objects.filter(query), mode="r")

    massform = LeadMassActionForm(request.user.get_profile())

    return render_to_response('sales/lead_index',
                              {'leads': leads,
                               'filters': filters,
                               'massform': massform,
                               'statuses': statuses
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_lead_form
def lead_index_assigned(request, response_format='html'):
    "Leads owned by current user"

    query = Q(status__hidden=False, assigned=request.user.get_profile())
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = query & _get_filter_query(request.GET)

    statuses = Object.filter_by_request(request, SaleStatus.objects, mode="r")
    leads = Object.filter_by_request(
        request, Lead.objects.filter(query), mode="r")
    filters = LeadFilterForm(request.user.get_profile(), '', request.GET)

    massform = LeadMassActionForm(request.user.get_profile())

    return render_to_response('sales/lead_index_assigned',
                              {'leads': leads,
                               'filters': filters,
                               'massform': massform,
                               'statuses': statuses
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def lead_add(request, lead_id=None, response_format='html'):
    "Lead add"

    all_leads = Object.filter_by_request(request, Lead.objects)

    if request.POST:
        if not 'cancel' in request.POST:
            lead = Lead()
            form = LeadForm(
                request.user.get_profile(), request.POST, instance=lead)
            if form.is_valid():
                lead = form.save()
                lead.set_user_from_request(request)
                return HttpResponseRedirect(reverse('sales_lead_view', args=[lead.id]))
        else:
            return HttpResponseRedirect(reverse('sales_lead_index'))
    else:
        form = LeadForm(request.user.get_profile())

    return render_to_response('sales/lead_add',
                              {'form': form,
                               'leads': all_leads},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def lead_edit(request, lead_id, response_format='html'):
    "Lead edit"

    lead = get_object_or_404(Lead, pk=lead_id)
    if not request.user.get_profile().has_permission(lead, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Lead", response_format)

    if request.POST:
        form = LeadForm(
            request.user.get_profile(), request.POST, instance=lead)
    else:
        form = LeadForm(request.user.get_profile(), instance=lead)
    if form.is_valid():
        lead = form.save()
        return HttpResponseRedirect(reverse('sales_lead_view', args=[lead.id]))

    return render_to_response('sales/lead_edit',
                              {'form': form,
                               'lead': lead,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def lead_view(request, lead_id, response_format='html'):
    "Queue view"
    profile = request.user.get_profile()
    lead = get_object_or_404(Lead, pk=lead_id)

    if not profile.has_permission(lead) \
            and not profile.is_admin('treeio.sales'):
        return user_denied(request, message="You don't have access to this Lead")

    form = _do_update_record(profile, request, lead)
    if form.is_valid():
        record = form.save()
        record.set_user_from_request(request)
        lead = record.object

    return render_to_response('sales/lead_view',
                              {'lead': lead,
                               'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def lead_delete(request, lead_id, response_format='html'):
    "Lead delete"

    lead = get_object_or_404(Lead, pk=lead_id)
    if not request.user.get_profile().has_permission(lead, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Sale Status", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                lead.trash = True
                lead.save()
            else:
                lead.delete()
            return HttpResponseRedirect(reverse('sales_lead_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('sales_lead_view', args=[lead.id]))

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))
    all_leads = Object.filter_by_request(request, Lead.objects)

    return render_to_response('sales/lead_delete',
                              {'lead': lead,
                               'leads': all_leads,
                               'products': all_products},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
@_process_mass_opportunity_form
def opportunity_index(request, response_format='html'):
    "Sales index page"

    query = Q(status__hidden=False)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = query & _get_filter_query(request.GET)

    filters = OpportunityFilterForm(
        request.user.get_profile(), '', request.GET)

    statuses = Object.filter_by_request(request, SaleStatus.objects, mode="r")
    opportunities = Object.filter_by_request(
        request, Opportunity.objects.filter(query), mode="r")

    massform = OpportunityMassActionForm(request.user.get_profile())

    return render_to_response('sales/opportunity_index',
                              {'opportunities': opportunities,
                               'filters': filters,
                               'massform': massform,
                               'statuses': statuses
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_opportunity_form
def opportunity_index_assigned(request, response_format='html'):
    "Opportunities owned by current user"

    query = Q(status__hidden=False, assigned=request.user.get_profile())
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = query & _get_filter_query(request.GET)

    statuses = Object.filter_by_request(request, SaleStatus.objects, mode="r")
    opportunities = Object.filter_by_request(
        request, Opportunity.objects.filter(query), mode="r")
    filters = OpportunityFilterForm(
        request.user.get_profile(), '', request.GET)

    massform = OpportunityMassActionForm(request.user.get_profile())

    return render_to_response('sales/opportunity_index_assigned',
                              {'opportunities': opportunities,
                               'filters': filters,
                               'massform': massform,
                               'statuses': statuses
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def opportunity_add(request, lead_id=None, response_format='html'):
    "Opportunity add"
    lead = None
    if lead_id:
        lead = get_object_or_404(Lead, pk=lead_id)

    if request.POST:
        if not 'cancel' in request.POST:
            form = OpportunityForm(
                request.user.get_profile(), lead, request.POST)
            if form.is_valid():
                opportunity = form.save(commit=False)
                convert(opportunity, 'amount')
                opportunity.set_user_from_request(request)
                return HttpResponseRedirect(reverse('sales_opportunity_view', args=[opportunity.id]))
        else:
            return HttpResponseRedirect(reverse('sales_opportunity_index'))
    else:
        form = OpportunityForm(request.user.get_profile(), lead)

    return render_to_response('sales/opportunity_add',
                              {'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def opportunity_edit(request, opportunity_id, response_format='html'):
    "Opportunity edit"

    opportunity = get_object_or_404(Opportunity, pk=opportunity_id)
    if not request.user.get_profile().has_permission(opportunity, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Opportunity", response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = OpportunityForm(
                request.user.get_profile(), None, request.POST, instance=opportunity)
            if form.is_valid():
                opportunity = form.save()
                convert(opportunity, 'amount')
                return HttpResponseRedirect(reverse('sales_opportunity_view', args=[opportunity.id]))
        else:
            return HttpResponseRedirect(reverse('sales_opportunity_view', args=[opportunity.id]))
    else:
        form = OpportunityForm(
            request.user.get_profile(), None, instance=opportunity)

    all_opportunities = Object.filter_by_request(request, Opportunity.objects)

    return render_to_response('sales/opportunity_edit',
                              {'form': form,
                               'opportunity': opportunity,
                               'opportunities': all_opportunities,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def opportunity_view(request, opportunity_id, response_format='html'):
    "Opportunity view"

    profile = request.user.get_profile()
    opportunity = get_object_or_404(Opportunity, pk=opportunity_id)
    if not profile.has_permission(opportunity) \
            and not profile.is_admin('treeio.sales'):
        return user_denied(request, message="You don't have access to this Opportunity")

    form = _do_update_record(profile, request, opportunity)

    return render_to_response('sales/opportunity_view',
                              {'opportunity': opportunity,
                               'record_form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def opportunity_delete(request, opportunity_id, response_format='html'):
    "Opportunity delete"

    opportunity = get_object_or_404(Opportunity, pk=opportunity_id)
    if not request.user.get_profile().has_permission(opportunity, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Sale Status", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                opportunity.trash = True
                opportunity.save()
            else:
                opportunity.delete()
            return HttpResponseRedirect(reverse('sales_opportunity_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('sales_opportunity_view', args=[opportunity.id]))

    all_opportunities = Object.filter_by_request(request, Opportunity.objects)

    return render_to_response('sales/opportunity_delete',
                              {'opportunity': opportunity,
                               'opportunities': all_opportunities,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def order_add(request, lead_id=None, opportunity_id=None, response_format='html'):
    "Order add"

    lead = None
    opportunity = None
    if lead_id:
        lead = get_object_or_404(Lead, pk=lead_id)
    if opportunity_id:
        opportunity = get_object_or_404(Opportunity, pk=opportunity_id)

    if request.POST:
        if not 'cancel' in request.POST:
            order = SaleOrder()
            form = OrderForm(
                request.user.get_profile(), lead, opportunity, request.POST, instance=order)
            if form.is_valid():
                order = form.save()
                order.set_user_from_request(request)
                return HttpResponseRedirect(reverse('sales_order_view', args=[order.id]))
        else:
            return HttpResponseRedirect(reverse('sales'))
    else:
        form = OrderForm(request.user.get_profile(), lead, opportunity)

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))

    return render_to_response('sales/order_add',
                              {'form': form,
                               'products': all_products},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def order_edit(request, order_id, response_format='html'):
    "SaleOrder edit"

    order = get_object_or_404(SaleOrder, pk=order_id)
    if not request.user.get_profile().has_permission(order, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this SaleOrder", response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = OrderForm(
                request.user.get_profile(), None, None, request.POST, instance=order)
            if form.is_valid():
                order = form.save()
                return HttpResponseRedirect(reverse('sales_order_view', args=[order.id]))
        else:
            return HttpResponseRedirect(reverse('sales_order_view', args=[order.id]))
    else:
        form = OrderForm(
            request.user.get_profile(), None, None, instance=order)

    all_orders = Object.filter_by_request(request, SaleOrder.objects)

    return render_to_response('sales/order_edit',
                              {'form': form,
                               'order': order,
                               'orders': all_orders,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def order_view(request, order_id, response_format='html'):
    "SaleOrder view"
    profile = request.user.get_profile()
    order = get_object_or_404(SaleOrder, pk=order_id)

    form = _do_update_record(profile, request, order)
    if form.is_valid():
        record = form.save()
        record.set_user_from_request(request)
        order = record.object

    if not profile.has_permission(order) \
            and not profile.is_admin('treeio.sales'):
        return user_denied(request, message="You don't have access to this Sale")

    ordered_products = order.orderedproduct_set.filter(trash=False)

    return render_to_response('sales/order_view',
                              {'order': order,
                               'ordered_products': ordered_products,
                               'record_form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def order_invoice_view(request, order_id, response_format='html'):
    "Order view as Invoice"
    order = get_object_or_404(SaleOrder, pk=order_id)
    if not request.user.get_profile().has_permission(order) \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, message="You don't have access to this Sale")

    ordered_products = order.orderedproduct_set.filter(trash=False)

    # default company
    try:
        conf = ModuleSetting.get_for_module('treeio.finance', 'my_company')[0]
        my_company = Contact.objects.get(pk=long(conf.value))

    except:
        my_company = None

    return render_to_response('sales/order_invoice_view',
                              {'order': order,
                               'ordered_products': ordered_products,
                               'my_company': my_company},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def order_delete(request, order_id, response_format='html'):
    "SaleOrder delete"

    order = get_object_or_404(SaleOrder, pk=order_id)
    if not request.user.get_profile().has_permission(order, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Sale Status", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                order.trash = True
                order.save()
            else:
                order.delete()
            return HttpResponseRedirect(reverse('sales_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('sales_order_view', args=[order.id]))

    all_orders = Object.filter_by_request(request, SaleOrder.objects)

    return render_to_response('sales/order_delete',
                              {'order': order,
                               'orders': all_orders,
                               },
                              context_instance=RequestContext(request), response_format=response_format)

#
# Settings
#


@treeio_login_required
@handle_response_format
def settings_view(request, response_format='html'):
    "Settings"

    if not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, message="You don't have administrator access to the Sales module")

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))
    all_statuses = Object.filter_by_request(request, SaleStatus.objects)
    all_sources = Object.filter_by_request(request, SaleSource.objects)

    # default currency
    try:
        default_currency = Currency.objects.get(is_default=True)
    except:
        default_currency = None

    # all currencies
    currencies = Object.filter_by_request(
        request, Currency.objects.filter(trash=False))

    # default lead status
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.sales', 'default_lead_status')[0]
        default_lead_status = SaleStatus.objects.get(pk=long(conf.value))
    except:
        default_lead_status = None

    # default opportunity status
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.sales', 'default_opportunity_status')[0]
        default_opportunity_status = SaleStatus.objects.get(
            pk=long(conf.value))
    except:
        default_opportunity_status = None

    # default order status
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.sales', 'default_order_status')[0]
        default_order_status = SaleStatus.objects.get(pk=long(conf.value))
    except:
        default_order_status = None

    # default order source
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.sales', 'default_order_source')[0]
        default_order_source = SaleSource.objects.get(pk=long(conf.value))
    except:
        default_order_source = None

    # order fulfilment status
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.sales', 'order_fulfil_status')[0]
        order_fulfil_status = SaleStatus.objects.get(pk=long(conf.value))
    except:
        order_fulfil_status = None

    # default product
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.sales', 'default_order_product')[0]
        default_order_product = Product.objects.get(pk=long(conf.value))
    except:
        default_order_product = None

    # check not trashed

    if default_opportunity_status:
        if default_opportunity_status.trash:
            default_opportunity_status = None
    if default_lead_status:
        if default_lead_status.trash:
            default_lead_status = None
    if default_order_status:
        if default_order_status.trash:
            default_order_status = None
    if default_order_source:
        if default_order_source.trash:
            default_order_source = None
    if order_fulfil_status:
        if order_fulfil_status.trash:
            order_fulfil_status = None
    if default_order_product:
        if default_order_product.trash:
            default_order_product = None

    return render_to_response('sales/settings_view',
                              {
                                  'products': all_products,
                                  'statuses': all_statuses,
                                  'sources': all_sources,
                                  'currencies': currencies,
                                  'default_opportunity_status': default_opportunity_status,
                                  'default_lead_status': default_lead_status,
                                  'default_order_status': default_order_status,
                                  'default_order_source': default_order_source,
                                  'order_fulfil_status': order_fulfil_status,
                                  'default_order_product': default_order_product,
                                  'default_currency': default_currency,
                              },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def settings_edit(request, response_format='html'):
    "Settings"

    if not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, message="You don't have administrator access to the Sales module")

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))

    if request.POST:
        if not 'cancel' in request.POST:
            form = SettingsForm(request.user.get_profile(), request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('sales_settings_view'))
        else:
            return HttpResponseRedirect(reverse('sales_settings_view'))
    else:
        form = SettingsForm(request.user.get_profile())

    return render_to_response('sales/settings_edit',
                              {
                                  'products': all_products,

                                  'form': form,
                              },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def status_add(request, response_format='html'):
    "TicketStatus add"

    if not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, message="You don't have administrator access to the Sales module")

    status = None
    if request.POST:
        if not 'cancel' in request.POST:
            status = SaleStatus()
            form = SaleStatusForm(
                request.user.get_profile(), request.POST, instance=status)
            if form.is_valid():
                status = form.save()
                status.set_user_from_request(request)
                return HttpResponseRedirect(reverse('sales_status_view', args=[status.id]))
        else:
            return HttpResponseRedirect(reverse('sales_settings_view'))
    else:
        form = SaleStatusForm(request.user.get_profile())

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))

    return render_to_response('sales/status_add',
                              {'form': form,
                               'status': status,
                               'products': all_products,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def status_view(request, status_id, response_format='html'):
    "Tickets filtered by status"

    status = get_object_or_404(SaleStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status) \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, message="You don't have access to this Sale Status")

    query = Q(status=status)
    if request.GET:
        query = query & _get_filter_query(request.GET)
    orders = Object.filter_by_request(request, SaleOrder.objects.filter(query))

    return render_to_response('sales/status_view',
                              {'status': status,
                               'orders': orders},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def status_edit(request, status_id, response_format='html'):
    "SaleStatus edit"

    status = get_object_or_404(SaleStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Sale Status", response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = SaleStatusForm(
                request.user.get_profile(), request.POST, instance=status)
            if form.is_valid():
                status = form.save()
                return HttpResponseRedirect(reverse('sales_status_view', args=[status.id]))
        else:
            return HttpResponseRedirect(reverse('sales_status_view', args=[status.id]))
    else:
        form = SaleStatusForm(request.user.get_profile(), instance=status)

    return render_to_response('sales/status_edit',
                              {'form': form,
                               'status': status},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def status_delete(request, status_id, response_format='html'):
    "SaleStatus delete"

    status = get_object_or_404(SaleStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Sale Status", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                status.trash = True
                status.save()
            else:
                status.delete()
            return HttpResponseRedirect(reverse('sales_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('sales_status_view', args=[status.id]))

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))

    return render_to_response('sales/status_delete',
                              {'status': status,
                               'products': all_products},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def source_add(request, response_format='html'):
    "TicketStatus add"

    if not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, message="You don't have administrator access to the Sales module")

    if request.POST:
        if not 'cancel' in request.POST:
            source = SaleSource()
            form = SaleSourceForm(
                request.user.get_profile(), request.POST, instance=source)
            if form.is_valid():
                source = form.save()
                source.set_user_from_request(request)
                return HttpResponseRedirect(reverse('sales_source_view', args=[source.id]))
        else:
            return HttpResponseRedirect(reverse('sales_settings_view'))
    else:
        form = SaleSourceForm(request.user.get_profile())

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))
    all_sources = Object.filter_by_request(request, SaleSource.objects)

    return render_to_response('sales/source_add',
                              {'form': form,
                               'sources': all_sources,
                               'products': all_products,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def source_view(request, source_id, response_format='html'):
    "Orders filtered by source"

    source = get_object_or_404(SaleSource, pk=source_id)
    if not request.user.get_profile().has_permission(source) \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, message="You don't have access to this Sale Status")

    query = Q(source=source)
    if request.GET:
        query = query & _get_filter_query(request.GET)
    orders = Object.filter_by_request(request, SaleOrder.objects.filter(query))

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))
    all_sources = Object.filter_by_request(request, SaleSource.objects)

    return render_to_response('sales/source_view',
                              {'source': source,
                               'sources': all_sources,
                               'products': all_products,
                               'orders': orders},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def source_edit(request, source_id, response_format='html'):
    "SaleSource edit"

    source = get_object_or_404(SaleSource, pk=source_id)
    if not request.user.get_profile().has_permission(source, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Sale Status", response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = SaleSourceForm(
                request.user.get_profile(), request.POST, instance=source)
            if form.is_valid():
                source = form.save()
                return HttpResponseRedirect(reverse('sales_source_view', args=[source.id]))
        else:
            return HttpResponseRedirect(reverse('sales_source_view', args=[source.id]))
    else:
        form = SaleSourceForm(request.user.get_profile(), instance=source)

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))
    all_sources = Object.filter_by_request(request, SaleSource.objects)

    return render_to_response('sales/source_edit',
                              {'form': form,
                               'source': source,
                               'sources': all_sources,
                               'products': all_products},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def source_delete(request, source_id, response_format='html'):
    "SaleSource delete"

    source = get_object_or_404(SaleSource, pk=source_id)
    if not request.user.get_profile().has_permission(source, mode='w') \
            and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, "You don't have access to this Sale Status", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                source.trash = True
                source.save()
            else:
                source.delete()
            return HttpResponseRedirect(reverse('sales_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('sales_source_view', args=[source.id]))

    all_products = Object.filter_by_request(
        request, Product.objects.filter(parent__isnull=True))
    all_sources = Object.filter_by_request(request, SaleSource.objects)

    return render_to_response('sales/source_delete',
                              {'source': source,
                               'sources': all_sources,
                               'products': all_products},
                              context_instance=RequestContext(request), response_format=response_format)


#
# AJAX handlers


@treeio_login_required
def ajax_subscription_lookup(request, response_format='html'):
    "Returns a list of matching tasks"

    subscriptions = []
    if request.GET and 'term' in request.GET:
        subscriptions = Subscription.objects.filter(
            Q(client__name__icontains=request.GET['term']) | Q(
                product__name__icontains=request.GET['term']) | Q(
                details__icontains=request.GET['term']))[:10]

    return render_to_response('sales/ajax_subscription_lookup',
                              {'subscriptions': subscriptions},
                              context_instance=RequestContext(request),
                              response_format=response_format)
#
