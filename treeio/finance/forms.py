# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Finance module forms
"""
from django.shortcuts import get_object_or_404
from django import forms
from treeio.identities.models import Contact
from treeio.finance.models import Transaction, Liability, Category, Account, Asset, Equity, Currency, Tax
from treeio.sales.models import SaleOrder
from treeio.core.models import Object, ModuleSetting
from django.core.urlresolvers import reverse
from treeio.core.decorators import preprocess_form
from django.utils.translation import ugettext as _
from treeio.sales.forms import standard_currencies

preprocess_form()


class MassActionForm(forms.Form):

    """ Mass action form for Transactions & Liabilities """

    category = forms.ModelChoiceField(queryset=[], required=False)
    delete = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                           ('trash', _('Move to Trash'))), required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)
        self.fields['delete'] = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'),
                                                                              ('delete', _(
                                                                                  'Delete Completely')),
                                                                              ('trash', _('Move to Trash'))), required=False)

        self.fields['category'].label = _("Category")
        self.fields['category'].queryset = Object.filter_permitted(
            user, Category.objects, mode='x')
        self.fields['category'].label = _("Add to Category:")

    def save(self, *args, **kwargs):
        "Process form"

        if self.instance:
            if self.is_valid():
                if self.cleaned_data['category']:
                    self.instance.category = self.cleaned_data['category']
                self.instance.save()
                if self.cleaned_data['delete']:
                    if self.cleaned_data['delete'] == 'delete':
                        self.instance.delete()
                    if self.cleaned_data['delete'] == 'trash':
                        self.instance.trash = True
                        self.instance.save()


class CategoryForm(forms.ModelForm):

    """ Category form """

    def __init__(self, user, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['details'].label = _("Details")

    class Meta:

        "Category Form"
        model = Category
        fields = ('name', 'details')


class AccountForm(forms.ModelForm):

    """ Account form """

    def __init__(self, user, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")

        self.fields['owner'].label = _("Owner")
        self.fields['owner'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['owner'].widget.attrs.update({'class': 'autocomplete',
                                                  'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['owner'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})

        self.fields['balance_currency'].label = _("Currency")
        self.fields['balance_currency'].widget.attrs.update(
            {'popuplink': reverse('finance_currency_add')})
        try:
            self.fields['balance_currency'].initial = Currency.objects.get(
                is_default=True)
        except:
            pass
        self.fields['balance_display'].label = _("Initial Balance")

        self.fields['details'].label = _("Details")

    class Meta:

        "Account Form"
        model = Account
        fields = (
            'name', 'owner', 'balance_currency', 'balance_display', 'details')


class AccountFilterForm(forms.ModelForm):

    """ Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(AccountFilterForm, self).__init__(*args, **kwargs)

        if 'owner' in skip:
            del self.fields['owner']
        else:
            self.fields['owner'].queryset = Object.filter_permitted(
                user, Contact.objects)
            self.fields['owner'].required = False
            self.fields['owner'].label = _("Owner")
            self.fields['owner'].help_text = ""
            self.fields['owner'].widget.attrs.update({'class': 'autocomplete',
                                                      'callback': reverse('identities_ajax_contact_lookup')})

    class Meta:

        "Account Filter Form"
        model = Account
        fields = ['owner']


class AssetForm(forms.ModelForm):

    """ Asset form """

    def __init__(self, user, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['asset_type'].label = _("Asset type")
        self.fields['initial_value'].label = _("Initial value")
        self.fields['lifetime'].label = _("Lifetime (years)")
        self.fields['endlife_value'].label = _("Endlife value")
        self.fields['depreciation_rate'].label = _("Depreciation rate")
        self.fields['purchase_date'].label = _("Purchase date")
        self.fields['purchase_date'].widget.attrs.update(
            {'class': 'datepicker'})
        self.fields['current_value'].label = _("Current value")
        self.fields['owner'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['owner'].widget.attrs.update({'class': 'autocomplete',
                                                  'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['owner'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})

    class Meta:

        "Asset Form"
        model = Asset
        fields = ('name', 'asset_type', 'initial_value', 'lifetime', 'endlife_value',
                  'depreciation_rate', 'depreciation_type', 'purchase_date', 'current_value', 'owner')


class AssetFilterForm(forms.ModelForm):

    """ Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(AssetFilterForm, self).__init__(*args, **kwargs)

        if 'purchase_date_from' in skip:
            del self.fields['purchase_date_from']
        else:
            self.fields['purchase_date_from'] = forms.DateField(label="Purchase Date From:",
                                                                required=False)
            self.fields['purchase_date_from'].widget.attrs.update(
                {'class': 'datepicker'})
            self.fields['purchase_date_from'].label = _("Purchase Date From")

        if 'purchase_date_to' in skip:
            del self.fields['purchase_date_to']
        else:
            self.fields['purchase_date_to'] = forms.DateField(
                label="Purchase Date To:", required=False)
            self.fields['purchase_date_to'].widget.attrs.update(
                {'class': 'datepicker'})
            self.fields['purchase_date_to'].label = _("Purchase Date To")

        if 'asset_type' in skip:
            del self.fields['asset_type']
        else:
            self.fields['asset_type'].label = _("Asset Type")
            self.fields['asset_type'].help_text = ""
            self.fields['asset_type'].required = False

        if 'owner' in skip:
            del self.fields['owner']
        else:
            self.fields['owner'].queryset = Object.filter_permitted(
                user, Contact.objects)
            self.fields['owner'].required = False
            self.fields['owner'].label = _("Owner")
            self.fields['owner'].help_text = ""
            self.fields['owner'].widget.attrs.update({'class': 'autocomplete',
                                                      'callback': reverse('identities_ajax_contact_lookup')})

    class Meta:

        "Asset Filter Form"
        model = Asset
        fields = ('owner', 'asset_type')


class EquityForm(forms.ModelForm):

    """ Equity form """

    def __init__(self, user, *args, **kwargs):
        super(EquityForm, self).__init__(*args, **kwargs)

        self.fields['equity_type'].label = _("Equity type")
        self.fields['issue_price'].label = _("Issue price")
        self.fields['sell_price'].label = _("Sell price")
        self.fields['issuer'].label = _("Issuer")
        self.fields['owner'].label = _("Owner")
        self.fields['amount'].label = _("Quantity")
        self.fields['purchase_date'].label = _("Purchase date")
        self.fields['details'].label = _("Details")

        self.fields['owner'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['owner'].widget.attrs.update({'class': 'autocomplete',
                                                  'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['owner'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['issuer'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['issuer'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['issuer'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.finance', 'my_company')[0]
            self.fields['issuer'].initial = long(conf.value)
        except Exception:
            pass

        self.fields['purchase_date'].widget.attrs.update(
            {'class': 'datepicker'})

    class Meta:

        "Equity Form"
        model = Equity
        fields = ('equity_type', 'issue_price', 'sell_price', 'issuer',
                  'owner', 'amount', 'purchase_date', 'details')


class EquityFilterForm(forms.ModelForm):

    """ Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(EquityFilterForm, self).__init__(*args, **kwargs)

        if 'purchase_date_from' in skip:
            del self.fields['purchase_date_from']
        else:
            self.fields['purchase_date_from'] = forms.DateField(label="Purchase Date From:",
                                                                required=False)
            self.fields['purchase_date_from'].widget.attrs.update(
                {'class': 'datepicker'})
            self.fields['purchase_date_from'].label = _("Purchase Date From")

        if 'purchase_date_to' in skip:
            del self.fields['purchase_date_to']
        else:
            self.fields['purchase_date_to'] = forms.DateField(
                label="Purchase Date To:", required=False)
            self.fields['purchase_date_to'].widget.attrs.update(
                {'class': 'datepicker'})
            self.fields['purchase_date_to'].label = _("Purchase Date To")

        if 'equity_type' in skip:
            del self.fields['equity_type']
        else:
            self.fields['equity_type'].label = _("Equity Type")
            self.fields['equity_type'].help_text = ""
            self.fields['equity_type'].required = False

        if 'issuer' in skip:
            del self.fields['issuer']
        else:
            self.fields['issuer'].queryset = Object.filter_permitted(
                user, Contact.objects)
            self.fields['issuer'].label = _("Issuer")
            self.fields['issuer'].help_text = ""
            self.fields['issuer'].required = False
            self.fields['issuer'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('identities_ajax_contact_lookup')})

        if 'owner' in skip:
            del self.fields['owner']
        else:
            self.fields['owner'].queryset = Object.filter_permitted(
                user, Contact.objects)
            self.fields['owner'].required = False
            self.fields['owner'].label = _("Owner")
            self.fields['owner'].help_text = ""
            self.fields['owner'].widget.attrs.update({'class': 'autocomplete',
                                                      'callback': reverse('identities_ajax_contact_lookup')})

    class Meta:

        "Equity Filter Form"
        model = Equity
        fields = ('issuer', 'owner', 'equity_type')


class ReceivableForm(forms.ModelForm):

    """ Receivable form """

    def __init__(self, user, *args, **kwargs):
        super(ReceivableForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['category'].label = _("Category")
        self.fields['source'].label = _("Source")
        self.fields['target'].label = _("Target")
        self.fields['account'].label = _("Bank Account")
        self.fields['due_date'].label = _("Due date")
        self.fields['value_currency'].label = _("Currency")
        self.fields['value_currency'].widget.attrs.update(
            {'popuplink': reverse('finance_currency_add')})
        self.fields['value_currency'].initial = Currency.objects.get(
            is_default=True)
        self.fields['value_display'].label = _("Value")
        self.fields['details'].label = _("Details")

        self.fields['source'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['source'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['source'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})

        self.fields['account'].queryset = Object.filter_permitted(
            user, Account.objects)

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.finance', 'default_account')[0]
            self.fields['account'].initial = long(conf.value)
        except Exception:
            pass

        self.fields['due_date'].widget.attrs.update({'class': 'datepicker'})

        del self.fields['target']

    class Meta:

        "Receivable Form"
        model = Liability
        fields = ('name', 'category', 'source', 'target', 'account',
                  'due_date', 'value_currency', 'value_display', 'details')


class TransactionForm(forms.ModelForm):

    """ Transaction form """

    def __init__(self, user, liability_id=None, order_id=None, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Description")
        self.fields['category'].label = _("Category")
        self.fields['source'].label = _("Source")
        self.fields['target'].label = _("Target")
        self.fields['account'].label = _("Bank Account")
        self.fields['datetime'].label = _("Date & Time")
        self.fields['value_currency'].label = _("Currency")
        self.fields['value_currency'].widget.attrs.update(
            {'popuplink': reverse('finance_currency_add')})
        self.fields['value_currency'].initial = Currency.objects.get(
            is_default=True)
        self.fields['value_display'].label = _("Value")
        self.fields['details'].label = _("Details")

        self.fields['source'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['target'].queryset = Object.filter_permitted(
            user, Contact.objects)

        self.fields['source'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['target'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})

        self.fields['source'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['target'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})

        self.fields['datetime'].widget.attrs.update(
            {'class': 'datetimepicker'})

        self.fields['account'].queryset = Object.filter_permitted(
            user, Account.objects)

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.finance', 'default_account')[0]
            self.fields['account'].initial = long(conf.value)
        except Exception:
            pass

        self.fields['liability'].queryset = Object.filter_permitted(
            user, Liability.objects)
        self.fields['liability'].label = _("Liability / Receivable")

        if order_id:
            order = get_object_or_404(SaleOrder, pk=order_id)
            self.fields['name'].initial = order.reference
            if order.client:
                self.fields['source'].initial = order.client

            # default company
            try:
                conf = ModuleSetting.get_for_module(
                    'treeio.finance', 'my_company')[0]
                self.fields['target'].initial = Contact.objects.get(
                    pk=long(conf.value))

            except Exception:
                pass
            self.fields['details'].initial = order.details
            self.fields['value_display'].initial = order.balance_due()
            self.fields['value_currency'].initial = order.currency

        if liability_id:
            self.fields['liability'].initial = liability_id
            liability = get_object_or_404(Liability, pk=liability_id)
            self.fields['name'].initial = liability.name
            self.fields['source'].initial = liability.source
            self.fields['target'].initial = liability.target
            self.fields['details'].initial = liability.details
            self.fields['category'].initial = liability.category
            self.fields['account'].initial = liability.account
            self.fields['value_display'].initial = liability.value_display
            self.fields['value_currency'].initial = liability.value_currency

    class Meta:

        "Transaction Form"
        model = Transaction
        fields = ('name', 'category', 'source', 'target', 'account',
                  'datetime', 'liability', 'value_currency', 'value_display', 'details')


class TransactionFilterForm(forms.ModelForm):

    """ Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(TransactionFilterForm, self).__init__(*args, **kwargs)

        if 'datefrom' in skip:
            del self.fields['datefrom']
            del self.fields['dateto']
        else:
            self.fields['datefrom'] = forms.DateField(
                label=_("Date From"), required=False)
            self.fields['datefrom'].widget.attrs.update(
                {'class': 'datepicker'})

        if 'dateto' in skip:
            del self.fields['dateto']
            del self.fields['datefrom']
        else:
            self.fields['dateto'] = forms.DateField(
                label=_("Date To"), required=False)
            self.fields['dateto'].widget.attrs.update({'class': 'datepicker'})

        if 'category' in skip:
            del self.fields['category']
        else:
            self.fields['category'].queryset = Object.filter_permitted(
                user, Category.objects)
            self.fields['category'].label = _("Category")
            self.fields['category'].help_text = ""
            self.fields['category'].required = False

        if 'source' in skip:
            del self.fields['source']
        else:
            self.fields['source'].queryset = Object.filter_permitted(
                user, Contact.objects)
            self.fields['source'].label = _("Source")
            self.fields['source'].help_text = ""
            self.fields['source'].required = False
            self.fields['source'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('identities_ajax_contact_lookup')})

        if 'target' in skip:
            del self.fields['target']
        else:
            self.fields['target'].queryset = Object.filter_permitted(
                user, Contact.objects)
            self.fields['target'].required = False
            self.fields['target'].label = _("Target")
            self.fields['target'].help_text = ""
            self.fields['target'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('identities_ajax_contact_lookup')})

    class Meta:

        "Transaction Filter Form"
        model = Transaction
        fields = ('category', 'source', 'target')


class LiabilityForm(forms.ModelForm):

    """ Folder form """

    def __init__(self, user, *args, **kwargs):
        super(LiabilityForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['category'].label = _("Category")
        self.fields['source'].label = _("Source")
        self.fields['target'].label = _("Target")
        self.fields['account'].label = _("Bank Account")
        self.fields['due_date'].label = _("Due date")
        self.fields['value_currency'].label = _("Currency")
        self.fields['value_currency'].widget.attrs.update(
            {'popuplink': reverse('finance_currency_add')})
        self.fields['value_currency'].initial = Currency.objects.get(
            is_default=True)
        self.fields['value_display'].label = _("Value")
        self.fields['details'].label = _("Details")

        self.fields['target'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['target'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['target'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})

        self.fields['account'].queryset = Object.filter_permitted(
            user, Account.objects)

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.finance', 'default_account')[0]
            self.fields['account'].initial = long(conf.value)
        except Exception:
            pass

        self.fields['due_date'].widget.attrs.update({'class': 'datepicker'})

        del self.fields['source']

    class Meta:

        "Liability Form"
        model = Liability
        fields = ('name', 'category', 'source', 'target', 'account',
                  'due_date', 'value_currency', 'value_display', 'details')


class LiabilityFilterForm(forms.ModelForm):

    """ Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(LiabilityFilterForm, self).__init__(*args, **kwargs)

        if 'due_date_from' in skip:
            del self.fields['due_date_from']
        else:
            self.fields['due_date_from'] = forms.DateField(
                label=_("Due Date From:"), required=False)
            self.fields['due_date_from'].widget.attrs.update(
                {'class': 'datepicker'})

        if 'due_date_to' in skip:
            del self.fields['due_date_to']
        else:
            self.fields['due_date_to'] = forms.DateField(
                label=_("Due Date To:"), required=False)
            self.fields['due_date_to'].widget.attrs.update(
                {'class': 'datepicker'})

        if 'category' in skip:
            del self.fields['category']
        else:
            self.fields['category'].queryset = Object.filter_permitted(
                user, Category.objects)
            self.fields['category'].label = _("Category")
            self.fields['category'].help_text = ""
            self.fields['category'].required = False

        if 'source' in skip:
            del self.fields['source']
        else:
            self.fields['source'].queryset = Object.filter_permitted(
                user, Contact.objects)
            self.fields['source'].label = _("Source")
            self.fields['source'].help_text = ""
            self.fields['source'].required = False
            self.fields['source'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('identities_ajax_contact_lookup')})

        if 'target' in skip:
            del self.fields['target']
        else:
            self.fields['target'].queryset = Object.filter_permitted(
                user, Contact.objects)
            self.fields['target'].required = False
            self.fields['target'].label = _("Target")
            self.fields['target'].help_text = ""
            self.fields['target'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('identities_ajax_contact_lookup')})

        if 'account' in skip:
            del self.fields['account']
        else:
            self.fields['account'].queryset = Object.filter_permitted(
                user, Account.objects)
            self.fields['account'].required = False
            self.fields['account'].label = _("Account")
            self.fields['account'].help_text = ""

    class Meta:

        "Liability Filter Form"
        model = Liability
        fields = ('category', 'source', 'target', 'account')


class SettingsForm(forms.Form):

    """ Administration settings form """

    default_currency = forms.ModelChoiceField(
        label='Base Currency', queryset=[])
    my_company = forms.ModelChoiceField(label='My Company', queryset=[])
    default_account = forms.ModelChoiceField(
        label='Default Account', queryset=[])

    def __init__(self, user, *args, **kwargs):
        "Sets choices and initial value"
        super(SettingsForm, self).__init__(*args, **kwargs)

        self.fields['my_company'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['my_company'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['default_account'].queryset = Object.filter_permitted(
            user, Account.objects)

        # Translation
        self.fields['default_currency'].label = _('Base Currency')
        self.fields['my_company'].label = _('My Company')
        self.fields['default_account'].label = _('Default Account')

        try:
            self.fields['default_currency'].widget.attrs.update(
                {'popuplink': reverse('finance_currency_add')})
            self.fields['default_currency'].queryset = Currency.objects.all()
            self.fields['default_currency'].initial = Currency.objects.get(
                is_default=True)
        except Exception:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.finance', 'my_company')[0]
            my_company = Contact.objects.get(pk=long(conf.value))
            self.fields['my_company'].initial = my_company.id
        except Exception:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.finance', 'default_account')[0]
            default_account = Account.objects.get(pk=long(conf.value))
            self.fields['default_account'].initial = default_account.id
        except Exception:
            pass

    def clean_my_company(self, *args, **kwargs):
        "Check that my company has an account"
        my_company = self.cleaned_data['my_company']

        if not my_company.account_set.count():
            raise forms.ValidationError(
                _("Your company has to have at least one Financial Account"))

        return my_company

    def clean_default_account(self):
        "Check that account owner is the same as my company"
        account = self.cleaned_data['default_account']
        try:
            company = self.cleaned_data['my_company']

            if not account.owner_id == company.id:
                raise forms.ValidationError(
                    _("Default Account has to belong to your company"))

        except KeyError:
            pass

        return account

    def save(self):
        "Form processor"
        try:
            ModuleSetting.set_for_module('my_company',
                                         self.cleaned_data['my_company'].id,
                                         'treeio.finance')
            ModuleSetting.set_for_module('default_account',
                                         self.cleaned_data[
                                             'default_account'].id,
                                         'treeio.finance')
            currency = Currency.objects.get(
                pk=self.cleaned_data['default_currency'])
            currency.is_default = True
            currency.save()
            return True

        except Exception:
            return False

#
# Currency
#


class CurrencyForm(forms.ModelForm):

    "Currency Form"

    code = forms.ChoiceField(
        label=_("Currency Code"), choices=standard_currencies)

    def __init__(self, user, *args, **kwargs):
        super(CurrencyForm, self).__init__(*args, **kwargs)

    class Meta:

        "Currency Form"
        model = Currency
        fields = ('name', 'code', 'symbol', 'factor')  # ,'is_active')

#
# Tax
#


class TaxForm(forms.ModelForm):

    "Tax Form"

    def __init__(self, user, *args, **kwargs):
        super(TaxForm, self).__init__(*args, **kwargs)

    class Meta:

        "Tax Form"
        model = Tax
        fields = ('name', 'rate', 'compound')
