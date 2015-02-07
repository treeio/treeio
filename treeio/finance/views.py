# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Finance Management module: views
"""
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum
from treeio.core.rendering import render_to_response
from treeio.core.models import Object, ModuleSetting
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.core.views import user_denied
from treeio.identities.models import Contact
from treeio.finance.forms import TransactionForm, LiabilityForm, AccountForm, EquityForm, AssetForm, \
    CategoryForm, MassActionForm, TransactionFilterForm, LiabilityFilterForm, \
    EquityFilterForm, AssetFilterForm, AccountFilterForm, ReceivableForm, \
    SettingsForm, CurrencyForm, TaxForm
from treeio.finance.models import Transaction, Liability, Category, Account, Equity, Asset, Currency, Tax
from treeio.finance.csvapi import ProcessTransactions
from treeio.sales.models import Product, SaleOrder
from treeio.sales.forms import dict_currencies
from treeio.finance.helpers import convert
from datetime import datetime, timedelta
from decimal import Decimal


def _get_filter_query(model, args):
    "Creates a query to filter Transactions based on FilterForm arguments"
    query = Q()

    for arg in args:
        if args[arg]:
            if hasattr(model, arg):
                kwargs = {str(arg + '__id'): long(args[arg])}
                query = query & Q(**kwargs)

    if 'datefrom' in args and args['datefrom']:
        datefrom = datetime.date(
            datetime.strptime(args['datefrom'], '%m/%d/%Y'))
        query = query & Q(date_created__gte=datefrom)

    if 'dateto' in args and args['dateto']:
        dateto = datetime.date(datetime.strptime(args['dateto'], '%m/%d/%Y'))
        query = query & Q(date_created__lte=dateto)

## Assets, Equities

    if 'purchase_date_from' in args and args['purchase_date_from']:
        purchase_date_from = datetime.date(
            datetime.strptime(args['purchase_date_from'], '%m/%d/%Y'))
        query = query & Q(purchase_date__gte=purchase_date_from)

    if 'purchase_date_to' in args and args['purchase_date_to']:
        purchase_date_to = datetime.date(
            datetime.strptime(args['purchase_date_to'], '%m/%d/%Y'))
        query = query & Q(purchase_date__lte=purchase_date_to)

## Liabilities, Receivables

    # Assets

    if 'due_date_from' in args and args['due_date_from']:
        due_date_from = datetime.date(
            datetime.strptime(args['due_date_from'], '%m/%d/%Y'))
        query = query & Q(due_date__gte=due_date_from)

    if 'due_date_to' in args and args['due_date_to']:
        due_date_to = datetime.date(
            datetime.strptime(args['due_date_to'], '%m/%d/%Y'))
        query = query & Q(due_date__lte=due_date_to)

    if 'equity_type' in args and args['equity_type']:
        equity_type = args['equity_type']
        query = query & Q(equity_type=equity_type)

    if 'asset_type' in args and args['asset_type']:
        asset_type = args['asset_type']
        query = query & Q(asset_type=asset_type)

    return query


#
# Categories
#

@handle_response_format
@treeio_login_required
def index_categories(request, response_format='html'):
    "Finance categories page"

    transactions = Object.filter_by_request(request, Transaction.objects)
    liabilities = Object.filter_by_request(request, Liability.objects)

    categories = Object.filter_by_request(request, Category.objects)

    return render_to_response('finance/index_categories',
                              {'categories': categories,
                               'transactions': transactions,
                               'liabilities': liabilities},
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def category_edit(request, category_id, response_format='html'):
    "category edit page"
    category = get_object_or_404(Category, pk=category_id)
    if request.POST:
        if not 'cancel' in request.POST:
            form = CategoryForm(
                request.user.get_profile(), request.POST, instance=category)
            if form.is_valid():
                category = form.save()
                return HttpResponseRedirect(reverse('finance_category_view', args=[category.id]))
        else:
            return HttpResponseRedirect(reverse('finance_category_view', args=[category.id]))
    else:
        form = CategoryForm(request.user.get_profile(), instance=category)
    return render_to_response('finance/category_edit',
                              {'form': form, 'category': category},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def category_add(request, response_format='html'):
    "new category form"
    categories = Object.filter_by_request(request, Category.objects, mode="r")
    if request.POST:
        if not 'cancel' in request.POST:
            category = Category()
            form = CategoryForm(
                request.user.get_profile(), request.POST, instance=category)
            if form.is_valid():
                category = form.save()
                category.set_user_from_request(request)
                return HttpResponseRedirect(reverse('finance_category_view', args=[category.id]))
        else:
            return HttpResponseRedirect(reverse('finance_categories'))
    else:
        form = CategoryForm(request.user.get_profile())
    return render_to_response('finance/category_add', {'form': form, 'categories': categories},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def category_view(request, category_id, response_format='html'):
    "Single category view page"
    category = get_object_or_404(Category, pk=category_id)

    if not request.user.get_profile().has_permission(category):
        return user_denied(request, message="You don't have access to this Category")

    if 'massform1' in request.POST:
        for key in request.POST:
            if 'mass-transaction' in key:
                try:
                    transaction = Transaction.objects.get(pk=request.POST[key])
                    form = MassActionForm(
                        request.user.get_profile(), request.POST, instance=transaction)
                    if form.is_valid() and request.user.get_profile().has_permission(transaction, mode='w'):
                        form.save()
                except Exception:
                    pass

    massform_transaction = MassActionForm(request.user.get_profile())

    if 'massform2' in request.POST:
        for key in request.POST:
            if 'mass-liability' in key:
                try:
                    liability = Liability.objects.get(pk=request.POST[key])
                    form = MassActionForm(
                        request.user.get_profile(), request.POST, instance=liability)
                    if form.is_valid() and request.user.get_profile().has_permission(liability, mode='w'):
                        form.save()
                except Exception:
                    pass

    massform_liability = MassActionForm(request.user.get_profile())

    transactions = Object.filter_by_request(request, Transaction.objects)
    liabilities = Object.filter_by_request(request, Liability.objects)

    return render_to_response('finance/category_view',
                              {'category': category,
                               'transactions': transactions,
                               'liabilities': liabilities,
                               'massform_transaction': massform_transaction,
                               'massform_liability': massform_liability},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def category_delete(request, category_id, response_format='html'):
    "Category delete"

    category = get_object_or_404(Category, pk=category_id)
    if not request.user.get_profile().has_permission(category, mode='w'):
        return user_denied(request, "You don't have access to this Category", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                category.trash = True
                category.save()
            else:
                category.delete()
            return HttpResponseRedirect(reverse('finance_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('finance_category_view', args=[category.id]))

    return render_to_response('finance/category_delete',
                              {'category': category},
                              context_instance=RequestContext(request), response_format=response_format)


#
# Accounts
#


@handle_response_format
@treeio_login_required
def account_edit(request, account_id, response_format='html'):
    "account edit page"
    account = get_object_or_404(Account, pk=account_id)
    if request.POST:
        if not 'cancel' in request.POST:
            form = AccountForm(
                request.user.get_profile(), request.POST, instance=account)
            if form.is_valid():
                account = form.save(commit=False)
                convert(account, 'balance')
                return HttpResponseRedirect(reverse('finance_account_view', args=[account.id]))
        else:
            return HttpResponseRedirect(reverse('finance_account_view', args=[account.id]))

    else:
        form = AccountForm(request.user.get_profile(), instance=account)
    return render_to_response('finance/account_edit',
                              {'form': form, 'account': account},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def account_add(request, response_format='html'):
    "new account form"
    if request.POST:
        if not 'cancel' in request.POST:
            account = Account()
            form = AccountForm(
                request.user.get_profile(), request.POST, instance=account)
            if form.is_valid():
                account = form.save(commit=False)
                convert(account, 'balance')
                account.set_user_from_request(request)
                return HttpResponseRedirect(reverse('finance_account_view', args=[account.id]))
        else:
            return HttpResponseRedirect(reverse('finance_index_accounts'))
    else:
        form = AccountForm(request.user.get_profile())
    return render_to_response('finance/account_add', {'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def account_view(request, account_id, response_format='html'):
    "Single transaction view page"
    account = get_object_or_404(Account, pk=account_id)
    return render_to_response('finance/account_view',
                              {'account': account},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def account_delete(request, account_id, response_format='html'):
    "Account delete"

    account = get_object_or_404(Account, pk=account_id)
    if not request.user.get_profile().has_permission(account, mode='w'):
        return user_denied(request, "You don't have access to this Account", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                account.trash = True
                account.save()
            else:
                account.delete()
            return HttpResponseRedirect(reverse('finance_index_accounts'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('finance_account_view', args=[account.id]))

    return render_to_response('finance/account_delete',
                              {'account': account},
                              context_instance=RequestContext(request), response_format=response_format)

#
# Assets
#


@handle_response_format
@treeio_login_required
def index_assets(request, response_format='html'):
    "Index_assets page: displays all Assets"

    if request.GET:
        query = _get_filter_query(Asset, request.GET)
    else:
        query = Q()

    filters = AssetFilterForm(request.user.get_profile(), 'title', request.GET)

    assets = Object.filter_by_request(
        request, Asset.objects.filter(query), mode="r")

    return render_to_response('finance/index_assets',
                              {'assets': assets,
                               'filters': filters
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def asset_edit(request, asset_id, response_format='html'):
    "asset edit page"
    asset = get_object_or_404(Asset, pk=asset_id)
    if request.POST:
        if not 'cancel' in request.POST:
            form = AssetForm(
                request.user.get_profile(), request.POST, instance=asset)
            if form.is_valid():
                asset = form.save()
                return HttpResponseRedirect(reverse('finance_asset_view', args=[asset.id]))
        else:
            return HttpResponseRedirect(reverse('finance_asset_view', args=[asset.id]))
    else:
        form = AssetForm(request.user.get_profile(), instance=asset)
    return render_to_response('finance/asset_edit',
                              {'form': form, 'asset': asset},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def asset_add(request, response_format='html'):
    "new asset form"
    assets = Object.filter_by_request(request, Asset.objects, mode="r")
    if request.POST:
        if not 'cancel' in request.POST:
            asset = Asset()
            form = AssetForm(
                request.user.get_profile(), request.POST, instance=asset)
            if form.is_valid():
                asset = form.save()
                asset.set_user_from_request(request)
                return HttpResponseRedirect(reverse('finance_asset_view', args=[asset.id]))
        else:
            return HttpResponseRedirect(reverse('finance_index_assets'))
    else:
        form = AssetForm(request.user.get_profile())
    return render_to_response('finance/asset_add', {'form': form, 'assets': assets},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def asset_view(request, asset_id, response_format='html'):
    "Single transaction view page"
    asset = get_object_or_404(Asset, pk=asset_id)
    return render_to_response('finance/asset_view',
                              {'asset': asset},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def asset_delete(request, asset_id, response_format='html'):
    "Asset delete"

    asset = get_object_or_404(Asset, pk=asset_id)
    if not request.user.get_profile().has_permission(asset, mode='w'):
        return user_denied(request, "You don't have access to this Asset", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                asset.trash = True
                asset.save()
            else:
                asset.delete()
            return HttpResponseRedirect(reverse('finance_index_assets'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('finance_asset_view', args=[asset.id]))

    return render_to_response('finance/asset_delete',
                              {'asset': asset},
                              context_instance=RequestContext(request), response_format=response_format)

#
# Equities
#


@handle_response_format
@treeio_login_required
def index_equities(request, response_format='html'):
    "Index_equities page: displays all Equities"
    if request.GET:
        query = _get_filter_query(Equity, request.GET)
    else:
        query = Q()

    filters = EquityFilterForm(
        request.user.get_profile(), 'title', request.GET)

    equities = Object.filter_by_request(
        request, Equity.objects.filter(query), mode="r")

    return render_to_response('finance/index_equities',
                              {'equities': equities,
                               'filters': filters
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def equity_edit(request, equity_id, response_format='html'):
    "equity edit page"
    equity = get_object_or_404(Equity, pk=equity_id)
    if request.POST:
        if not 'cancel' in request.POST:
            form = EquityForm(
                request.user.get_profile(), request.POST, instance=equity)
            if form.is_valid():
                equity = form.save()
                return HttpResponseRedirect(reverse('finance_equity_view', args=[equity.id]))
        else:
            return HttpResponseRedirect(reverse('finance_equity_view', args=[equity.id]))
    else:
        form = EquityForm(request.user.get_profile(), instance=equity)
    return render_to_response('finance/equity_edit',
                              {'form': form, 'equity': equity},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def equity_add(request, response_format='html'):
    "new equity form"
    equities = Object.filter_by_request(request, Equity.objects, mode="r")
    if request.POST:
        if not 'cancel' in request.POST:
            equity = Equity()
            form = EquityForm(
                request.user.get_profile(), request.POST, instance=equity)
            if form.is_valid():
                equity = form.save()
                equity.set_user_from_request(request)
                return HttpResponseRedirect(reverse('finance_equity_view', args=[equity.id]))
        else:
            return HttpResponseRedirect(reverse('finance_index_equities'))
    else:
        form = EquityForm(request.user.get_profile())
    return render_to_response('finance/equity_add', {'form': form, 'equities': equities},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def equity_view(request, equity_id, response_format='html'):
    "Single transaction view page"
    equity = get_object_or_404(Equity, pk=equity_id)
    return render_to_response('finance/equity_view',
                              {'equity': equity},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def equity_delete(request, equity_id, response_format='html'):
    "Equity delete"

    equity = get_object_or_404(Equity, pk=equity_id)
    if not request.user.get_profile().has_permission(equity, mode='w'):
        return user_denied(request, "You don't have access to this Equity", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                equity.trash = True
                equity.save()
            else:
                equity.delete()
            return HttpResponseRedirect(reverse('finance_index_equities'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('finance_equity_view', args=[equity.id]))

    return render_to_response('finance/equity_delete',
                              {'equity': equity},
                              context_instance=RequestContext(request), response_format=response_format)

#
# Transactions
#


@handle_response_format
@treeio_login_required
def index_transactions(request, response_format='html'):
    "Index_transactions page: displays all Transactions"
    if request.GET:
        query = _get_filter_query(Transaction, request.GET)
    else:
        query = Q()

    if 'massform' in request.POST:
        for key in request.POST:
            if 'mass-transaction' in key:
                try:
                    transaction = Transaction.objects.get(pk=request.POST[key])
                    form = MassActionForm(
                        request.user.get_profile(), request.POST, instance=transaction)
                    if form.is_valid() and request.user.get_profile().has_permission(transaction, mode='w'):
                        form.save()
                except:
                    pass

    massform = MassActionForm(request.user.get_profile())

    transactions = Object.filter_by_request(
        request, Transaction.objects.filter(query), mode="r")

    filters = TransactionFilterForm(
        request.user.get_profile(), 'title', request.GET)

    return render_to_response('finance/index_transactions',
                              {'transactions': transactions,
                               'massform': massform,
                               'filters': filters
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def transaction_add(request, liability_id=None, order_id=None, response_format='html'):
    "new transaction form"
    transactions = Object.filter_by_request(
        request, Transaction.objects, mode="r")
    if request.POST:
        if not 'cancel' in request.POST:
            transaction = Transaction()
            form = TransactionForm(
                request.user.get_profile(), None, None, request.POST, instance=transaction)
            if form.is_valid():
                transaction = form.save(commit=False)
                convert(transaction, 'value')
                transaction.set_user_from_request(request)
                if order_id:
                    try:
                        order = SaleOrder.objects.get(pk=order_id)
                        order.payment.add(transaction)
                        order.save()
                    except:
                        pass
                return HttpResponseRedirect(reverse('finance_transaction_view', args=[transaction.id]))
        else:
            return HttpResponseRedirect(reverse('finance_index_transactions'))
    else:
        form = TransactionForm(
            request.user.get_profile(), liability_id=liability_id, order_id=order_id)
    return render_to_response('finance/transaction_add', {'form': form, 'transactions': transactions},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def transaction_edit(request, transaction_id, response_format='html'):
    "Transaction edit page"
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.POST:
        if not 'cancel' in request.POST:
            form = TransactionForm(
                request.user.get_profile(), None, None, request.POST, instance=transaction)
            if form.is_valid():
                transaction = form.save(commit=False)
                convert(transaction, 'value')
                return HttpResponseRedirect(reverse('finance_transaction_view', args=[transaction.id]))
        else:
            return HttpResponseRedirect(reverse('finance_transaction_view', args=[transaction.id]))
    else:
        form = TransactionForm(
            request.user.get_profile(), None, None, instance=transaction)
    return render_to_response('finance/transaction_edit',
                              {'form': form, 'transaction': transaction},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def transaction_view(request, transaction_id, response_format='html'):
    "Single transaction view page"
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    return render_to_response('finance/transaction_view',
                              {'transaction': transaction},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def transaction_delete(request, transaction_id, response_format='html'):
    "Transaction delete"

    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if not request.user.get_profile().has_permission(transaction, mode='w'):
        return user_denied(request, "You don't have access to this Transaction", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                transaction.trash = True
                transaction.save()
            else:
                transaction.delete()
            return HttpResponseRedirect(reverse('finance_index_transactions'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('finance_transaction_view', args=[transaction.id]))

    return render_to_response('finance/transaction_delete',
                              {'transaction': transaction},
                              context_instance=RequestContext(request), response_format=response_format)
#
# Liabilities
#


@handle_response_format
@treeio_login_required
def index_liabilities(request, response_format='html'):
    "Index_liabilities page: displays all Liabilities"
    if request.GET:
        query = _get_filter_query(Liability, request.GET)
    else:
        query = Q()

    if 'massform' in request.POST:
        for key in request.POST:
            if 'mass-liability' in key:
                try:
                    liability = Liability.objects.get(pk=request.POST[key])
                    form = MassActionForm(
                        request.user.get_profile(), request.POST, instance=liability)
                    if form.is_valid() and request.user.get_profile().has_permission(liability, mode='w'):
                        form.save()
                except Exception:
                    pass

    massform = MassActionForm(request.user.get_profile())

    filters = LiabilityFilterForm(
        request.user.get_profile(), 'title', request.GET)

    liabilities = Object.filter_by_request(
        request, Liability.objects.filter(query), mode="r")

    template_liabilities = []
    for liability in liabilities:
        if liability.account.owner_id == liability.source_id:
            template_liabilities.append(liability)

    return render_to_response('finance/index_liabilities',
                              {'liabilities': template_liabilities,
                               'massform': massform,
                               'filters': filters
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def liability_edit(request, liability_id, response_format='html'):
    "liability edit page"
    liability = get_object_or_404(Liability, pk=liability_id)
    if request.POST:
        if not 'cancel' in request.POST:
            form = LiabilityForm(
                request.user.get_profile(), request.POST, instance=liability)
            if form.is_valid():
                liability = form.save(commit=False)
                convert(liability, 'value')
                return HttpResponseRedirect(reverse('finance_liability_view', args=[liability.id]))
        else:
            return HttpResponseRedirect(reverse('finance_liability_view', args=[liability.id]))
    else:
        form = LiabilityForm(request.user.get_profile(), instance=liability)
    return render_to_response('finance/liability_edit',
                              {'form': form, 'liability': liability},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def liability_add(request, response_format='html'):
    "new liability form"
    liabilities = Object.filter_by_request(
        request, Liability.objects, mode="r")
    if request.POST:
        if not 'cancel' in request.POST:
            liability = Liability()
            form = LiabilityForm(
                request.user.get_profile(), request.POST, instance=liability)
            if form.is_valid():
                liability = form.save(commit=False)
                liability.source = liability.account.owner
                convert(liability, 'value')
                liability.set_user_from_request(request)
                return HttpResponseRedirect(reverse('finance_liability_view', args=[liability.id]))
        else:
            return HttpResponseRedirect(reverse('finance_index_liabilities'))
    else:
        form = LiabilityForm(request.user.get_profile())
    return render_to_response('finance/liability_add', {'form': form, 'liabilities': liabilities},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def liability_view(request, liability_id, response_format='html'):
    "Single transaction view page"
    liability = get_object_or_404(Liability, pk=liability_id)

    transactions = liability.transaction_set.all()

    return render_to_response('finance/liability_view',
                              {'liability': liability,
                               'transactions': transactions},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def liability_delete(request, liability_id, response_format='html'):
    "Liability delete"

    liability = get_object_or_404(Liability, pk=liability_id)
    if not request.user.get_profile().has_permission(liability, mode='w'):
        return user_denied(request, "You don't have access to this Liability", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                liability.trash = True
                liability.save()
            else:
                liability.delete()
            return HttpResponseRedirect(reverse('finance_index_liabilities'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('finance_liability_view', args=[liability.id]))

    return render_to_response('finance/liability_delete',
                              {'liability': liability},
                              context_instance=RequestContext(request), response_format=response_format)


#
# Receivables
#

@handle_response_format
@treeio_login_required
def index_receivables(request, response_format='html'):
    "Index_receivables page: displays all Liabilities"
    if request.GET:
        query = _get_filter_query(Liability, request.GET)
    else:
        query = Q()

    if 'massform' in request.POST:
        for key in request.POST:
            if 'mass-liability' in key:
                try:
                    liability = Liability.objects.get(pk=request.POST[key])
                    form = MassActionForm(
                        request.user.get_profile(), request.POST, instance=liability)
                    if form.is_valid() and request.user.get_profile().has_permission(liability, mode='w'):
                        form.save()
                except Exception:
                    pass

    massform = MassActionForm(request.user.get_profile())

    filters = LiabilityFilterForm(
        request.user.get_profile(), 'title', request.GET)

    receivables = Object.filter_by_request(
        request, Liability.objects.filter(query), mode="r")

    template_receivables = []
    for receivable in receivables:
        if receivable.account.owner_id == receivable.target_id:
            template_receivables.append(receivable)

    return render_to_response('finance/index_receivables',
                              {'liabilities': template_receivables,
                               'filters': filters,
                               'massform': massform},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def receivable_add(request, response_format='html'):
    "new receivable form"
    if request.POST:
        if not 'cancel' in request.POST:
            receivable = Liability()
            form = ReceivableForm(
                request.user.get_profile(), request.POST, instance=receivable)
            if form.is_valid():
                receivable = form.save(commit=False)
                receivable.target = receivable.account.owner
                convert(receivable, 'value')
                receivable.set_user_from_request(request)
                return HttpResponseRedirect(reverse('finance_receivable_view', args=[receivable.id]))
        else:
            return HttpResponseRedirect(reverse('finance_index_receivables'))
    else:
        form = ReceivableForm(request.user.get_profile())
    return render_to_response('finance/receivable_add', {'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def receivable_edit(request, receivable_id, response_format='html'):
    "Liability edit page"
    receivable = get_object_or_404(Liability, pk=receivable_id)
    if request.POST:
        if not 'cancel' in request.POST:
            form = ReceivableForm(
                request.user.get_profile(), request.POST, instance=receivable)
            if form.is_valid():
                receivable = form.save(commit=False)
                convert(receivable, 'value')
                return HttpResponseRedirect(reverse('finance_receivable_view', args=[receivable.id]))
        else:
            return HttpResponseRedirect(reverse('finance_receivable_view', args=[receivable.id]))
    else:
        form = ReceivableForm(request.user.get_profile(), instance=receivable)
    return render_to_response('finance/receivable_edit',
                              {'form': form, 'liability': receivable},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def receivable_view(request, receivable_id, response_format='html'):
    "Single receivable view page"
    receivable = get_object_or_404(Liability, pk=receivable_id)
    transactions = receivable.transaction_set.all()

    return render_to_response('finance/receivable_view',
                              {'liability': receivable,
                               'transactions': transactions},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def receivable_delete(request, receivable_id, response_format='html'):
    "Receivable delete"

    receivable = get_object_or_404(Liability, pk=receivable_id)
    if not request.user.get_profile().has_permission(receivable, mode='w'):
        return user_denied(request, "You don't have access to this Receivable", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                receivable.trash = True
                receivable.save()
            else:
                receivable.delete()
            return HttpResponseRedirect(reverse('finance_index_receivables'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('finance_receivable_view', args=[receivable.id]))

    return render_to_response('finance/receivable_delete',
                              {'liability': receivable},
                              context_instance=RequestContext(request), response_format=response_format)

#
# Reports
#


@handle_response_format
@treeio_login_required
def income_view(request, response_format='html'):
    "Income Statement view page"

    try:
        conf = ModuleSetting.get_for_module('treeio.finance', 'my_company')[0]
        my_company = Contact.objects.get(pk=long(conf.value), trash=False)

    except Exception:
        my_company = None

    if my_company:
        categories = Category.objects.filter(trash=False)
        transactions = Transaction.objects.filter(
            account__owner=my_company, trash=False)
    else:
        categories = Object.filter_by_request(request, Category.objects)
        transactions = Object.filter_by_request(request, Transaction.objects)

    total = 0
    revenues = 0
    expenses = 0

    if my_company:
        # Receivables
        for receivable in Liability.objects.filter(target=my_company, trash=False):
            value = receivable.value
            paid = receivable.transaction_set.filter(
                source=my_company, trash=False).aggregate(Sum('value'))
            if paid['value__sum']:
                value = receivable.value - paid['value__sum']
            if value > 0:
                revenues += value
                total += value

                for category in categories:
                    if receivable.category == category:
                        category.revenue += value

    # Actual Transactions
    for transaction in transactions:
        val = transaction.get_relative_value()
        total += val
        if val > 0:
            revenues += val
        else:
            expenses += abs(val)

    for category in categories:
        for transaction in transactions:
            if transaction.category == category:
                val = transaction.get_relative_value()
                if val > 0:
                    category.revenue += val
                else:
                    category.expense += abs(val)

    return render_to_response('finance/income_view',
                              {'transactions': transactions,
                               'categories': categories,
                               'total': total,
                               'revenues': revenues,
                               'expenses': expenses
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def balance_sheet(request, response_format='html'):
    "Balance Sheet view page"

    balance = {'assets_fixed': Decimal('0.0'),
               'assets_intangible': Decimal('0.0'),
               'assets_inventories': Decimal('0.0'),
               'assets_receivables': Decimal('0.0'),
               'assets_prepayments': Decimal('0.0'),
               'assets_cash': Decimal('0.0'),
               'assets_total': Decimal('0.0'),
               'liabilities_borrowings': Decimal('0.0'),
               'liabilities_payables': Decimal('0.0'),
               'liabilities_total': Decimal('0.0'),
               'equity_share_capital': Decimal('0.0'),
               'equity_share_premium': Decimal('0.0'),
               'equity_retained': Decimal('0.0'),
               'equity_total': Decimal('0.0'),
               'equity_liabilities_total': Decimal('0.0')}

    try:
        conf = ModuleSetting.get_for_module('treeio.finance', 'my_company')[0]
        my_company = Contact.objects.get(pk=long(conf.value), trash=False)
    except:
        my_company = None

    if my_company:

        # Assets Fixed and Intangible
        for asset in Asset.objects.filter(owner=my_company, current_value__gt=0, trash=False):
            if asset.asset_type == 'fixed':
                balance['assets_fixed'] += asset.current_value
            elif asset.asset_type == 'intangible':
                balance['assets_intangible'] += asset.current_value

        # Inventories
        for product in Product.objects.filter(active=True, buy_price__isnull=False, stock_quantity__gt=0,
                                              trash=False):
            balance['assets_inventories'] += product.buy_price * \
                product.stock_quantity

        # Receivables
        for receivable in Liability.objects.filter(target=my_company, trash=False):
            value = receivable.value
            paid = receivable.transaction_set.filter(
                source=my_company, trash=False).aggregate(Sum('value'))
            if paid['value__sum']:
                value = receivable.value - paid['value__sum']
            balance['assets_receivables'] += value
            balance['equity_retained'] += value

        # Assets Cash
        for account in Account.objects.filter(owner=my_company, trash=False):
            account_balance = account.get_balance()
            if account_balance > 0:
                balance['assets_cash'] += account_balance

        # Prepayments (and Liabilities, since retrieving Liabilities anyway)
        for liability in Liability.objects.filter(source=my_company, trash=False):
            value = liability.value
            paid = liability.transaction_set.filter(
                source=my_company, trash=False).aggregate(Sum('value'))
            if paid['value__sum']:
                value = liability.value - paid['value__sum']
            if value > 0:
                # If Due Date is more than a year from now, that's a borrowing
                if liability.due_date and liability.due_date >= (datetime.today() + timedelta(days=365)).date():
                    balance['liabilities_borrowings'] += value
                else:
                    balance['liabilities_payables'] += value
            else:
                balance['assets_prepayments'] += -value

        # Assets Total
        balance['assets_total'] = balance['assets_fixed']
        balance['assets_total'] += balance['assets_intangible']
        balance['assets_total'] += balance['assets_inventories']
        balance['assets_total'] += balance['assets_receivables']
        balance['assets_total'] += balance['assets_prepayments']
        balance['assets_total'] += balance['assets_cash']

        # Liabilities Total
        balance['liabilities_total'] += balance['liabilities_borrowings']
        balance['liabilities_total'] += balance['liabilities_payables']

        # Shares
        for share in Equity.objects.filter(issuer=my_company, trash=False):
            capital = share.issue_price * share.amount
            premium = (share.sell_price - share.issue_price) * share.amount
            balance['equity_share_capital'] += capital
            balance['equity_share_premium'] += premium

        # Retained Revenues calculated out of Transactions
        for transaction in Transaction.objects.filter(account__owner=my_company, trash=False):
            balance['equity_retained'] += transaction.get_relative_value()

        # Total Equities
        balance['equity_total'] = balance['equity_share_capital']
        balance['equity_total'] += balance['equity_share_premium']
        balance['equity_total'] += balance['equity_retained']

        # Total Equities + Liabilities
        balance['equity_liabilities_total'] = balance[
            'equity_total'] + balance['liabilities_total']

    context = {'company': my_company, 'today': datetime.today(), 'red': False}
    if balance['equity_liabilities_total'] != balance['assets_total']:
        context['red'] = True

    context.update(balance)

    return render_to_response('finance/balance_sheet', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# Settings
#
@handle_response_format
@treeio_login_required
def index_accounts(request, response_format='html'):
    "Settings"

    if not request.user.get_profile().is_admin('treeio.finance'):
        return user_denied(request, message="You don't have administrator access to the Finance module")

    if request.GET:
        query = _get_filter_query(Account, request.GET)
    else:
        query = Q()

    filters = AccountFilterForm(
        request.user.get_profile(), 'title', request.GET)

    all_accounts = Object.filter_by_request(
        request, Account.objects.filter(query))

    return render_to_response('finance/index_accounts',
                              {
                                  'accounts': all_accounts,
                                  'filters': filters
                              },
                              context_instance=RequestContext(request), response_format=response_format)

#
# Settings
#


@treeio_login_required
@handle_response_format
def settings_view(request, response_format='html'):
    "Settings"

    # default currency
    if not request.user.get_profile().is_admin('treeio.finance'):
        return user_denied(request, message="You don't have administrator access to the Finance module")

    try:
        default_currency = Currency.objects.get(is_default=True)
    except Exception:
        default_currency = "$"

    # default company
    try:
        conf = ModuleSetting.get_for_module('treeio.finance', 'my_company')[0]
        my_company = Contact.objects.get(pk=long(conf.value))

    except Exception:
        my_company = None

    # default account
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.finance', 'default_account')[0]
        default_account = Account.objects.get(pk=long(conf.value))
    except Exception:
        default_account = None

    # check not trashed
    if my_company:
        if my_company.trash:
            my_company = None
    if default_account:
        if default_account.trash:
            default_account = None

    categories = Object.filter_by_request(
        request, Category.objects.filter(trash=False))

    # all currencies
    currencies = Object.filter_by_request(
        request, Currency.objects.filter(trash=False))

    if request.GET and 'export' in request.GET:
        transactions = Transaction.objects.filter(trash=False)
        # Export all contacts into a CSV file
        export = ProcessTransactions()
        return export.export_transactions(transactions)

    if request.POST:
        if 'file' in request.FILES:
            csv_file = request.FILES['file']

            # TODO: check file extension
            content = csv_file.read()
            Import = ProcessTransactions()
            Import.import_transactions(content)

    return render_to_response('finance/settings_view',
                              {
                                  'default_account': default_account,
                                  'default_currency': default_currency,
                                  'my_company': my_company,
                                  'categories': categories,
                                  'currencies': currencies,
                              },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def settings_edit(request, response_format='html'):
    "Settings"

    if not request.user.get_profile().is_admin('treeio.finance'):
        return user_denied(request, message="You don't have administrator access to the Finance module")

    if request.POST:
        if not 'cancel' in request.POST:
            form = SettingsForm(request.user.get_profile(), request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('finance_settings_view'))
        else:
            return HttpResponseRedirect(reverse('finance_settings_view'))
    else:
        form = SettingsForm(request.user.get_profile())

    return render_to_response('finance/settings_edit',
                              {
                                  'form': form,
                              },
                              context_instance=RequestContext(request), response_format=response_format)


#
# Currency
#

@treeio_login_required
@handle_response_format
def currency_add(request, response_format='html'):
    "Currency add"

    if not request.user.get_profile().is_admin('treeio.finance'):
        return user_denied(request, message="You don't have administrator access to the Finance module")

    if request.POST:
        if not 'cancel' in request.POST:
            currency = Currency()
            form = CurrencyForm(
                request.user.get_profile(), request.POST, instance=currency)
            if form.is_valid():
                currency = form.save(commit=False)
                cname = dict_currencies[currency.code]
                currency.name = cname[cname.index(' ') + 2:]
                # currency.factor = 1.0 #Get currency conversion here
                currency.save()
                currency.set_user_from_request(request)
                return HttpResponseRedirect(reverse('finance_currency_view', args=[currency.id]))
        else:
            return HttpResponseRedirect(reverse('finance_settings_view'))
    else:
        form = CurrencyForm(request.user.get_profile())

    return render_to_response('finance/currency_add',
                              {'form': form,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def currency_edit(request, currency_id, response_format='html'):
    "Currency edit"

    currency = get_object_or_404(Currency, pk=currency_id)
    if not request.user.get_profile().has_permission(currency, mode='w') \
            and not request.user.get_profile().is_admin('treeio_finance'):
        return user_denied(request, "You don't have access to this Currency", response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = CurrencyForm(
                request.user.get_profile(), request.POST, instance=currency)
            if form.is_valid():
                currency = form.save()
                return HttpResponseRedirect(reverse('finance_currency_view', args=[currency.id]))
        else:
            return HttpResponseRedirect(reverse('finance_currency_view', args=[currency.id]))
    else:
        form = CurrencyForm(request.user.get_profile(), instance=currency)

    return render_to_response('finance/currency_edit',
                              {'form': form,
                               'currency': currency},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def currency_view(request, currency_id, response_format='html'):
    "View a currency"

    currency = get_object_or_404(Currency, pk=currency_id)
    if not request.user.get_profile().has_permission(currency, mode='r') \
            and not request.user.get_profile().is_admin('treeio_finance'):
        return user_denied(request, "You don't have access to this Currency", response_format)

    return render_to_response('finance/currency_view',
                              {'currency': currency},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def currency_delete(request, currency_id, response_format='html'):
    "Currency delete"

    currency = get_object_or_404(Currency, pk=currency_id)
    if not request.user.get_profile().has_permission(currency, mode='w'):
        return user_denied(request, "You don't have access to this Currency", response_format)

    if currency.is_default:
        return user_denied(request, "You cannot delete the Base Currency", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                currency.trash = True
                currency.save()
            else:
                currency.delete()
            return HttpResponseRedirect(reverse('finance_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('finance_currency_view', args=[currency.id]))

    return render_to_response('finance/currency_delete',
                              {'currency': currency},
                              context_instance=RequestContext(request), response_format=response_format)

#
# Tax
#


@treeio_login_required
@handle_response_format
def tax_add(request, response_format='html'):
    "Tax add"

    if not request.user.get_profile().is_admin('treeio.finance'):
        return user_denied(request, message="You don't have administrator access to the Finance module")

    if request.POST:
        if not 'cancel' in request.POST:
            tax = Tax()
            form = TaxForm(
                request.user.get_profile(), request.POST, instance=tax)
            if form.is_valid():
                tax = form.save()
                tax.set_user_from_request(request)
                return HttpResponseRedirect(reverse('finance_tax_view', args=[tax.id]))
        else:
            return HttpResponseRedirect(reverse('finance_settings_view'))
    else:
        form = TaxForm(request.user.get_profile())

    return render_to_response('finance/tax_add',
                              {'form': form,
                               },
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def tax_edit(request, tax_id, response_format='html'):
    "Tax edit"

    tax = get_object_or_404(Tax, pk=tax_id)
    if not request.user.get_profile().has_permission(tax, mode='w') \
            and not request.user.get_profile().is_admin('treeio_finance'):
        return user_denied(request, "You don't have access to this Tax", response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = TaxForm(
                request.user.get_profile(), request.POST, instance=tax)
            if form.is_valid():
                tax = form.save()
                return HttpResponseRedirect(reverse('finance_tax_view', args=[tax.id]))
        else:
            return HttpResponseRedirect(reverse('finance_tax_view', args=[tax.id]))
    else:
        form = TaxForm(request.user.get_profile(), instance=tax)

    return render_to_response('finance/tax_edit',
                              {'form': form,
                               'tax': tax},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def tax_view(request, tax_id, response_format='html'):
    "View a tax"

    tax = get_object_or_404(Tax, pk=tax_id)
    if not request.user.get_profile().has_permission(tax, mode='r') \
            and not request.user.get_profile().is_admin('treeio_finance'):
        return user_denied(request, "You don't have access to this Tax", response_format)

    return render_to_response('finance/tax_view',
                              {'tax': tax},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def tax_delete(request, tax_id, response_format='html'):
    "Tax delete"

    tax = get_object_or_404(Tax, pk=tax_id)
    if not request.user.get_profile().has_permission(tax, mode='w'):
        return user_denied(request, "You don't have access to this Tax", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                tax.trash = True
                tax.save()
            else:
                tax.delete()
            return HttpResponseRedirect(reverse('finance_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('finance_tax_view', args=[tax.id]))

    return render_to_response('finance/tax_delete',
                              {'tax': tax},
                              context_instance=RequestContext(request), response_format=response_format)
