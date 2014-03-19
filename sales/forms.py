# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

# -*- coding: utf-8 -*-
"""
Sales module forms
"""
from django.shortcuts import get_object_or_404
from django import forms
from django.db.models import Q
from treeio.sales.models import Product, SaleOrder, SaleSource, Lead, Opportunity, \
    SaleStatus, OrderedProduct, Subscription, Currency
from treeio.identities.models import Contact
from treeio.core.models import Object, ModuleSetting, User, UpdateRecord
from django.core.urlresolvers import reverse
from treeio.core.decorators import preprocess_form
from django.utils.translation import ugettext as _

preprocess_form()

standard_currencies = (
    ("AED", "AED  United Arab Emirates, Dirhams"),
    ("AFN", "AFN  Afghanistan, Afghanis"),
    ("ALL", "ALL  Albania, Leke"),
    ("AMD", "AMD  Armenia, Drams"),
    ("ANG", "ANG  Netherlands Antilles, Guilders (also called Florins)"),
    ("AOA", "AOA  Angola, Kwanza"),
    ("ARS", "ARS  Argentina, Pesos"),
    ("AUD", "AUD  Australia, Dollars"),
    ("AWG", "AWG  Aruba, Guilders (also called Florins)"),
    ("AZN", "AZN  Azerbaijan, New Manats"),
    ("BAM", "BAM  Bosnia and Herzegovina, Convertible Marka"),
    ("BBD", "BBD  Barbados, Dollars"),
    ("BDT", "BDT  Bangladesh, Taka"),
    ("BGN", "BGN  Bulgaria, Leva"),
    ("BHD", "BHD  Bahrain, Dinars"),
    ("BIF", "BIF  Burundi, Francs"),
    ("BMD", "BMD  Bermuda, Dollars"),
    ("BND", "BND  Brunei Darussalam, Dollars"),
    ("BOB", "BOB  Bolivia, Bolivianos"),
    ("BRL", "BRL  Brazil, Brazil Real"),
    ("BSD", "BSD  Bahamas, Dollars"),
    ("BTN", "BTN  Bhutan, Ngultrum"),
    ("BWP", "BWP  Botswana, Pulas"),
    ("BYR", "BYR  Belarus, Rubles"),
    ("BZD", "BZD  Belize, Dollars"),
    ("CAD", "CAD  Canada, Dollars"),
    ("CDF", "CDF  Congo/Kinshasa, Congolese Francs"),
    ("CHF", "CHF  Switzerland, Francs"),
    ("CLP", "CLP  Chile, Pesos"),
    ("CNY", "CNY  China, Yuan Renminbi"),
    ("COP", "COP  Colombia, Pesos"),
    ("CRC", "CRC  Costa Rica, Colones"),
    ("CUP", "CUP  Cuba, Pesos"),
    ("CVE", "CVE  Cape Verde, Escudos"),
    ("CZK", "CZK  Czech Republic, Koruny"),
    ("DJF", "DJF  Djibouti, Francs"),
    ("DKK", "DKK  Denmark, Kroner"),
    ("DOP", "DOP  Dominican Republic, Pesos"),
    ("DZD", "DZD  Algeria, Algeria Dinars"),
    ("EGP", "EGP  Egypt, Pounds"),
    ("ERN", "ERN  Eritrea, Nakfa"),
    ("ETB", "ETB  Ethiopia, Birr"),
    ("EUR", "EUR  Euro Member Countries, Euro"),
    ("FJD", "FJD  Fiji, Dollars"),
    ("FKP", "FKP  Falkland Islands (Malvinas), Pounds"),
    ("GBP", "GBP  United Kingdom, Pounds"),
    ("GEL", "GEL  Georgia, Lari"),
    ("GGP", "GGP  Guernsey, Pounds"),
    ("GHS", "GHS  Ghana, Cedis"),
    ("GIP", "GIP  Gibraltar, Pounds"),
    ("GMD", "GMD  Gambia, Dalasi"),
    ("GNF", "GNF  Guinea, Francs"),
    ("GTQ", "GTQ  Guatemala, Quetzales"),
    ("GYD", "GYD  Guyana, Dollars"),
    ("HKD", "HKD  Hong Kong, Dollars"),
    ("HNL", "HNL  Honduras, Lempiras"),
    ("HRK", "HRK  Croatia, Kuna"),
    ("HTG", "HTG  Haiti, Gourdes"),
    ("HUF", "HUF  Hungary, Forint"),
    ("IDR", "IDR  Indonesia, Rupiahs"),
    ("ILS", "ILS  Israel, New Shekels"),
    ("IMP", "IMP  Isle of Man, Pounds"),
    ("INR", "INR  India, Rupees"),
    ("IQD", "IQD  Iraq, Dinars"),
    ("IRR", "IRR  Iran, Rials"),
    ("ISK", "ISK  Iceland, Kronur"),
    ("JEP", "JEP  Jersey, Pounds"),
    ("JMD", "JMD  Jamaica, Dollars"),
    ("JOD", "JOD  Jordan, Dinars"),
    ("JPY", "JPY  Japan, Yen"),
    ("KES", "KES  Kenya, Shillings"),
    ("KGS", "KGS  Kyrgyzstan, Soms"),
    ("KHR", "KHR  Cambodia, Riels"),
    ("KMF", "KMF  Comoros, Francs"),
    ("KPW", "KPW  Korea (North), Won"),
    ("KRW", "KRW  Korea (South), Won"),
    ("KWD", "KWD  Kuwait, Dinars"),
    ("KYD", "KYD  Cayman Islands, Dollars"),
    ("KZT", "KZT  Kazakhstan, Tenge"),
    ("LAK", "LAK  Laos, Kips"),
    ("LBP", "LBP  Lebanon, Pounds"),
    ("LKR", "LKR  Sri Lanka, Rupees"),
    ("LRD", "LRD  Liberia, Dollars"),
    ("LSL", "LSL  Lesotho, Maloti"),
    ("LTL", "LTL  Lithuania, Litai"),
    ("LVL", "LVL  Latvia, Lati"),
    ("LYD", "LYD  Libya, Dinars"),
    ("MAD", "MAD  Morocco, Dirhams"),
    ("MDL", "MDL  Moldova, Lei"),
    ("MGA", "MGA  Madagascar, Ariary"),
    ("MKD", "MKD  Macedonia, Denars"),
    ("MMK", "MMK  Myanmar (Burma), Kyats"),
    ("MNT", "MNT  Mongolia, Tugriks"),
    ("MOP", "MOP  Macau, Patacas"),
    ("MRO", "MRO  Mauritania, Ouguiyas"),
    ("MUR", "MUR  Mauritius, Rupees"),
    ("MVR", "MVR  Maldives (Maldive Islands), Rufiyaa"),
    ("MWK", "MWK  Malawi, Kwachas"),
    ("MXN", "MXN  Mexico, Pesos"),
    ("MYR", "MYR  Malaysia, Ringgits"),
    ("MZN", "MZN  Mozambique, Meticais"),
    ("NAD", "NAD  Namibia, Dollars"),
    ("NGN", "NGN  Nigeria, Nairas"),
    ("NIO", "NIO  Nicaragua, Cordobas"),
    ("NOK", "NOK  Norway, Krone"),
    ("NPR", "NPR  Nepal, Nepal Rupees"),
    ("NZD", "NZD  New Zealand, Dollars"),
    ("OMR", "OMR  Oman, Rials"),
    ("PAB", "PAB  Panama, Balboa"),
    ("PEN", "PEN  Peru, Nuevos Soles"),
    ("PGK", "PGK  Papua New Guinea, Kina"),
    ("PHP", "PHP  Philippines, Pesos"),
    ("PKR", "PKR  Pakistan, Rupees"),
    ("PLN", "PLN  Poland, Zlotych"),
    ("PYG", "PYG  Paraguay, Guarani"),
    ("QAR", "QAR  Qatar, Rials"),
    ("RON", "RON  Romania, New Lei"),
    ("RSD", "RSD  Serbia, Dinars"),
    ("RUB", "RUB  Russia, Rubles"),
    ("RWF", "RWF  Rwanda, Rwanda Francs"),
    ("SAR", "SAR  Saudi Arabia, Riyals"),
    ("SBD", "SBD  Solomon Islands, Dollars"),
    ("SCR", "SCR  Seychelles, Rupees"),
    ("SDG", "SDG  Sudan, Pounds"),
    ("SEK", "SEK  Sweden, Kronor"),
    ("SGD", "SGD  Singapore, Dollars"),
    ("SHP", "SHP  Saint Helena, Pounds"),
    ("SLL", "SLL  Sierra Leone, Leones"),
    ("SOS", "SOS  Somalia, Shillings"),
    ("SPL", "SPL  Seborga, Luigini"),
    ("SRD", "SRD  Suriname, Dollars"),
    ("STD", "STD  Sao Tome and Principe, Dobras"),
    ("SVC", "SVC  El Salvador, Colones"),
    ("SYP", "SYP  Syria, Pounds"),
    ("SZL", "SZL  Swaziland, Emalangeni"),
    ("THB", "THB  Thailand, Baht"),
    ("TJS", "TJS  Tajikistan, Somoni"),
    ("TMM", "TMM  Turkmenistan, Manats"),
    ("TND", "TND  Tunisia, Dinars"),
    ("TOP", "TOP  Tonga, Pa'anga"),
    ("TRY", "TRY  Turkey, New Lira"),
    ("TTD", "TTD  Trinidad and Tobago, Dollars"),
    ("TVD", "TVD  Tuvalu, Tuvalu Dollars"),
    ("TWD", "TWD  Taiwan, New Dollars"),
    ("TZS", "TZS  Tanzania, Shillings"),
    ("UAH", "UAH  Ukraine, Hryvnia"),
    ("UGX", "UGX  Uganda, Shillings"),
    ("USD", "USD  United States of America, Dollars"),
    ("UYU", "UYU  Uruguay, Pesos"),
    ("UZS", "UZS  Uzbekistan, Sums"),
    ("VEF", "VEF  Venezuela, Bolivares Fuertes"),
    ("VND", "VND  Viet Nam, Dong"),
    ("VUV", "VUV  Vanuatu, Vatu"),
    ("WST", "WST  Samoa, Tala"),
    ("XAF", "XAF  Communaute Financiere Africaine BEAC, Francs"),
    ("XAG", "XAG  Silver, Ounces"),
    ("XAU", "XAU  Gold, Ounces"),
    ("XCD", "XCD  East Caribbean Dollars"),
    ("XDR", "XDR  International Monetary Fund (IMF) Special Drawing Rights"),
    ("XOF", "XOF  Communaute Financiere Africaine BCEAO, Francs"),
    ("XPD", "XPD  Palladium Ounces"),
    ("XPF", "XPF  Comptoirs Francais du Pacifique Francs"),
    ("XPT", "XPT  Platinum, Ounces"),
    ("YER", "YER  Yemen, Rials"),
    ("ZAR", "ZAR  South Africa, Rand"),
    ("ZMK", "ZMK  Zambia, Kwacha"),
    ("ZWD", "ZWD  Zimbabwe, Zimbabwe Dollars")
)

dict_currencies = dict(standard_currencies)


class SettingsForm(forms.Form):

    """ Administration settings form """

    default_currency = forms.ModelChoiceField(
        label=_('Base Currency'), queryset=Currency.objects)
    default_lead_status = forms.ModelChoiceField(
        label=_('Default Lead Status'), queryset=[])
    default_opportunity_status = forms.ModelChoiceField(
        label=_('Default Opportunity Status'), queryset=[])
    default_order_status = forms.ModelChoiceField(
        label=_('Default Order Status'), queryset=[])
    default_order_source = forms.ModelChoiceField(
        label=_('Default Order Source'), queryset=[])
    default_order_product = forms.ModelChoiceField(
        label=_('Default Order Product'), queryset=[], required=False)
    order_fulfil_status = forms.ModelChoiceField(
        label=_('Order Fulfilment Status'), queryset=[])

    def __init__(self, user, *args, **kwargs):
        "Sets choices and initial value"
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['default_lead_status'].queryset = Object.filter_permitted(user,
                                                                              SaleStatus.objects.filter(use_leads=True))
        self.fields['default_opportunity_status'].queryset = Object.filter_permitted(user,
                                                                                     SaleStatus.objects.filter(use_opportunities=True))
        self.fields['default_order_status'].queryset = Object.filter_permitted(user,
                                                                               SaleStatus.objects.filter(use_sales=True))
        self.fields['default_order_source'].queryset = Object.filter_permitted(user,
                                                                               SaleSource.objects.all())
        self.fields['order_fulfil_status'].queryset = Object.filter_permitted(user,
                                                                              SaleStatus.objects.filter(use_sales=True))
        self.fields['default_order_product'].queryset = Object.filter_permitted(user,
                                                                                Product.objects.filter(active=True))

        # Translation

        self.fields['default_currency'].label = _('Base Currency')
        self.fields['default_lead_status'].label = _('Default Lead Status')
        self.fields['default_opportunity_status'].label = _(
            'Default Opportunity Status')
        self.fields['default_order_status'].label = _('Default Order Status')
        self.fields['default_order_source'].label = _('Default Order Source')
        self.fields['default_order_product'].label = _('Default Order Product')
        self.fields['order_fulfil_status'].label = _('Order Fulfilment Status')

        try:
            self.fields['default_currency'].queryset = Currency.objects
            self.fields['default_currency'].initial = Currency.objects.get(
                is_default__exact=True)
            self.fields['default_currency'].widget.attrs.update(
                {'popuplink': reverse('sales_currency_add')})
        except:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_opportunity_status')[0]
            default_opportunity_status = SaleStatus.objects.get(
                pk=long(conf.value))
            self.fields[
                'default_opportunity_status'].initial = default_opportunity_status.id
        except:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_lead_status')[0]
            default_lead_status = SaleStatus.objects.get(pk=long(conf.value))
            self.fields['default_lead_status'].initial = default_lead_status.id
        except:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_order_status')[0]
            default_order_status = SaleStatus.objects.get(pk=long(conf.value))
            self.fields[
                'default_order_status'].initial = default_order_status.id
        except:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_order_source')[0]
            default_order_source = SaleSource.objects.get(pk=long(conf.value))
            self.fields[
                'default_order_source'].initial = default_order_source.id
        except:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_order_product')[0]
            default_order_product = Product.objects.get(pk=long(conf.value))
            self.fields[
                'default_order_product'].initial = default_order_product.id
        except:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'order_fulfil_status')[0]
            order_fulfil_status = SaleStatus.objects.get(pk=long(conf.value))
            self.fields['order_fulfil_status'].initial = order_fulfil_status.id
        except:
            pass

    def save(self):
        "Form processor"
        fields = self.fields
        try:
            for field in fields:
                if self.cleaned_data[field]:
                    if field == 'default_currency':
                        ModuleSetting.set_for_module('default_currency',
                                                     self.cleaned_data[
                                                         'default_currency'],
                                                     'treeio.sales')
                        currency = Currency.objects.get(
                            pk=self.cleaned_data['default_currency'])
                        currency.is_default = True
                        currency.save()
                    else:
                        ModuleSetting.set_for_module(field, self.cleaned_data[field].id,
                                                     'treeio.sales')
            return True
        except:
            return False


class MassActionForm(forms.Form):

    """ Mass action form for Orders """

    status = forms.ModelChoiceField(queryset=[], required=False)
    assignedto = forms.ModelChoiceField(queryset=[], required=False)
    delete = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                           ('trash', _('Move to Trash'))), required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)

        self.fields['status'].queryset = Object.filter_permitted(user,
                                                                 SaleStatus.objects.filter(
                                                                     use_sales=True),
                                                                 mode='x')
        self.fields['status'].label = _("Status:")
        self.fields['delete'] = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'),
                                                                              ('delete', _(
                                                                                  'Delete Completely')),
                                                                              ('trash', _('Move to Trash'))), required=False)

        self.fields['assignedto'].queryset = User.objects
        self.fields['assignedto'].label = _("Assign To:")
        # self.fields['assignedto'].widget.attrs.update({'class': 'autocomplete',
        #                                               'callback': reverse('identities_ajax_user_lookup')})

    def save(self, *args, **kwargs):
        "Process form"

        if self.instance:
            if self.is_valid():
                if self.cleaned_data['status']:
                    self.instance.status = self.cleaned_data['status']
                if self.cleaned_data['assignedto']:
                    self.instance.assigned.add(self.cleaned_data['assignedto'])
                self.instance.save()
                if self.cleaned_data['delete']:
                    if self.cleaned_data['delete'] == 'delete':
                        self.instance.delete()
                    if self.cleaned_data['delete'] == 'trash':
                        self.instance.trash = True
                        self.instance.save()


class LeadMassActionForm(forms.Form):

    """ Mass action form for Orders """

    status = forms.ModelChoiceField(queryset=[], required=False)
    assignedto = forms.ModelChoiceField(queryset=[], required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(LeadMassActionForm, self).__init__(*args, **kwargs)

        self.fields['status'].queryset = Object.filter_permitted(user,
                                                                 SaleStatus.objects.filter(
                                                                     use_leads=True),
                                                                 mode='x')
        self.fields['status'].label = _("Status:")

        self.fields['assignedto'].queryset = User.objects
        self.fields['assignedto'].label = _("Assign To:")
       # self.fields['assignedto'].widget.attrs.update({'class': 'autocomplete',
       #                                                'callback': reverse('identities_ajax_user_lookup')})

    def save(self, *args, **kwargs):
        "Process form"

        if self.instance:
            if self.is_valid():
                if self.cleaned_data['status']:
                    self.instance.status = self.cleaned_data['status']
                if self.cleaned_data['assignedto']:
                    self.instance.assigned.add(self.cleaned_data['assignedto'])
                self.instance.save()


class OpportunityMassActionForm(forms.Form):

    """ Mass action form for Orders """

    status = forms.ModelChoiceField(queryset=[], required=False)
    assignedto = forms.ModelChoiceField(queryset=[], required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(OpportunityMassActionForm, self).__init__(*args, **kwargs)

        self.fields['status'].queryset = Object.filter_permitted(user,
                                                                 SaleStatus.objects.filter(
                                                                     use_opportunities=True),
                                                                 mode='x')
        self.fields['status'].label = _("Status:")

        self.fields['assignedto'].queryset = User.objects
        self.fields['assignedto'].label = _("Assign To:")
     #   self.fields['assignedto'].widget.attrs.update({'class': 'autocomplete',
     #                                                  'callback': reverse('identities_ajax_user_lookup')})

    def save(self, *args, **kwargs):
        "Process form"

        if self.instance:
            if self.is_valid():
                if self.cleaned_data['status']:
                    self.instance.status = self.cleaned_data['status']
                if self.cleaned_data['assignedto']:
                    self.instance.assigned.add(self.cleaned_data['assignedto'])
                self.instance.save()


class ProductMassActionForm(forms.Form):

    """ Mass action form for Products """

    active = forms.ChoiceField(label=_("Action"), choices=(('', '-------'), ('active', 'Mark as Active'),
                                                           ('inactive', 'Mark as Inactive')), required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(ProductMassActionForm, self).__init__(*args, **kwargs)

        # Translation
        self.fields['active'].label = _("Action")

    def save(self, *args, **kwargs):
        "Process form"
        if self.instance:
            if self.is_valid():
                if self.cleaned_data['active'] == 'active':
                    self.instance.active = True
                if self.cleaned_data['active'] == 'inactive':
                    self.instance.active = False
                self.instance.save()


class SaleStatusForm(forms.ModelForm):

    """ Status form """
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

    def __init__(self, user, *args, **kwargs):
        super(SaleStatusForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['use_leads'].label = _("Enabled for Leads")
        self.fields['use_opportunities'].label = _("Enabled for Opportunities")
        self.fields['use_sales'].label = _("Enabled for Sales")

        self.fields['active'].label = _("Active")
        self.fields['hidden'].label = _("Hidden")
        self.fields['details'].label = _("Details")

        self.fields['active'].initial = True

    class Meta:

        "Sales Status Form"
        model = SaleStatus
        fields = ('name', 'use_leads', 'use_opportunities',
                  'use_sales', 'active', 'hidden', 'details')


class SaleSourceForm(forms.ModelForm):

    """ Status form """
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

    def __init__(self, user, *args, **kwargs):
        super(SaleSourceForm, self).__init__(*args, **kwargs)

        self.fields['active'].initial = True
        self.fields['name'].label = _("Name")
        self.fields['active'].label = _("Active")
        self.fields['details'].label = _("Details")

    class Meta:

        "Sale Source Form"
        model = SaleSource
        fields = ('name', 'active', 'details')


class ProductForm(forms.ModelForm):

    """ Product form """
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

    def __init__(self, user, parent=None, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['supplier'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['supplier'].widget.attrs.update({'class': 'autocomplete',
                                                     'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['supplier'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['supplier'].label = _("Supplier")
        self.fields['active'].initial = True
        self.fields['active'].label = _("Active")

        manager = Product.objects.filter(active=True)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            manager = manager.exclude(Q(parent=instance) & Q(pk=instance.id))
        self.fields['parent'].queryset = Object.filter_permitted(
            user, manager, mode='x')

        if parent:
            self.fields['parent'].initial = get_object_or_404(
                Product, pk=parent)
            self.fields['parent'].label = _("Parent")

        self.fields['product_type'].label = _("Product type")
        self.fields['code'].label = _("Code")
        self.fields['supplier_code'].label = _("Supplier code")
        self.fields['buy_price'].label = _("Buy price")
        self.fields['sell_price'].label = _("Sell price")
        self.fields['stock_quantity'].label = _("Stock quantity")
        self.fields['runout_action'].label = _("Runout action")
        self.fields['details'].label = _("Details")

    class Meta:

        "ProductForm"
        model = Product
        fields = ('name', 'parent', 'product_type', 'code', 'supplier', 'supplier_code', 'buy_price',
                  'sell_price', 'stock_quantity', 'active', 'runout_action', 'details')


class ProductFilterForm(forms.ModelForm):

    """ Ticket Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(ProductFilterForm, self).__init__(*args, **kwargs)

        self.fields['product_type'].queryset = Object.filter_permitted(user,
                                                                       Product.objects.filter(active=True))
        self.fields['product_type'].required = False
        self.fields['product_type'].label = _("Product type")

        self.fields['supplier'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['supplier'].required = False
        self.fields['supplier'].widget.attrs.update({'class': 'autocomplete',
                                                     'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['supplier'].label = _("Supplier")

        self.fields['active'].required = False
        self.fields['active'].initial = True
        self.fields['active'].label = _("Active")

    class Meta:

        "Product Filter Form"
        model = Product
        fields = ('product_type', 'supplier', 'active')


class UpdateRecordForm(forms.ModelForm):

    "UpdateRecord form"

    def __init__(self, *args, **kwargs):
        super(UpdateRecordForm, self).__init__(*args, **kwargs)

        self.fields['body'].label = _("Details")
        self.fields['body'].required = True

    class Meta:

        "UpdateRecordForm"
        model = UpdateRecord
        fields = ['body']


class OrderedProductForm(forms.ModelForm):

    """ Add New Ordered Product """

    def __init__(self, user, order, *args, **kwargs):

        super(OrderedProductForm, self).__init__(*args, **kwargs)

        self.fields['subscription'].queryset = Object.filter_permitted(
            user, Subscription.objects)
        self.fields['subscription'].widget.attrs.update({'class': 'autocomplete',
                                                         'callback': reverse('sales_ajax_subscription_lookup')})
        self.fields['subscription'].widget.attrs.update(
            {'popuplink': reverse('sales_subscription_add')})
        self.fields['subscription'].label = _("Subscription")

        self.fields['product'].queryset = Object.filter_permitted(
            user, Product.objects.filter(active=True))
        if user.is_admin('treeio.sales'):
            self.fields['product'].widget.attrs.update(
                {'popuplink': reverse('sales_product_add')})
            self.fields['product'].label = _("Product")

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_order_product')[0]
            # AJAX to set the initial rate as the currency converted value of
            # product sell price
            self.fields['product'].initial = long(conf.value)
        except:
            pass

        # Tax
        self.fields['tax'].widget.attrs.update(
            {'popuplink': reverse('finance_tax_add')})

        # TODO: rate
        #  self.fields['rate_display'].label = _("Rate")
        #  self.fields['rate_display'].help_text = order.currency.code

        self.fields['quantity'].label = _("Quantity")
        self.fields['quantity'].initial = 1
        self.fields['discount'].label = _("Discount")
        self.fields['discount'].help_text = "%"

    def save(self, *args, **kwargs):
        "Set Rate"
        instance = super(OrderedProductForm, self).save(commit=False)
        if 'product' in self.cleaned_data and self.cleaned_data['product']:
            instance.rate = self.cleaned_data['product'].sell_price
            instance.rate_display = instance.rate

        return instance

    class Meta:

        "OrderedProductForm"
        model = OrderedProduct
        fields = ('product', 'quantity', 'subscription',
                  'tax', 'discount', 'description')


class SubscriptionForm(forms.ModelForm):

    """ Add New Subscription """

    def __init__(self, user, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)

        del self.fields['cycle_end']

        self.fields['product'].queryset = Object.filter_permitted(
            user, Product.objects)
        self.fields['product'].label = _("Product")

        self.fields['client'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['client'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['client'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['client'].label = _("Client")

        self.fields['start'].widget.attrs.update({'class': 'datepicker'})
        self.fields['start'].label = _("Start")
        self.fields['expiry'].widget.attrs.update({'class': 'datepicker'})
        self.fields['expiry'].label = _("Expiry")

        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            self.fields['start'].widget.attrs['readonly'] = True
            del kwargs['instance']

        self.fields['active'].initial = True
        self.fields['active'].label = _("Active")
        self.fields['cycle_period'].label = _("Cycle period")
        self.fields['details'].label = _("Details")

    class Meta:

        "Subscription Form"
        model = Subscription
        fields = ('client', 'product', 'start', 'expiry',
                  'cycle_period', 'cycle_end', 'active', 'details')


class OrderForm(forms.ModelForm):

    """ Order form """

    def __init__(self, user, lead=None, opportunity=None, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['reference'].required = False
        self.fields['reference'].label = _("Reference")
        if hasattr(self, 'instance') and not self.instance.reference:
            next_ref = self.instance.get_next_reference()
            if next_ref:
                self.fields['reference'].initial = next_ref

        self.fields['client'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['client'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['client'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['client'].label = _("Client")

        self.fields['source'].queryset = Object.filter_permitted(
            user, SaleSource.objects.filter(active=True))
        self.fields['source'].label = _("Source")

        # Currency
        self.fields['currency'].label = _('Currency')
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            del self.fields['currency']
        else:
            self.fields['currency'].widget.attrs.update(
                {'popuplink': reverse('finance_currency_add')})
            self.fields['currency'].initial = Currency.objects.get(
                is_default=True)

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_order_source')[0]
            self.fields['source'].initial = long(conf.value)
        except:
            pass

        self.fields['status'].queryset = Object.filter_permitted(user,
                                                                 SaleStatus.objects.filter(use_sales=True))
        self.fields['status'].label = _("Status")

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_order_status')[0]
            self.fields['status'].initial = long(conf.value)
        except:
            pass

        if opportunity:
            self.fields['opportunity'].queryset = Object.filter_permitted(
                user, Opportunity.objects)
            self.fields['opportunity'].label = _("Opportunity")
            self.fields['opportunity'].initial = opportunity.id
            self.fields['client'].initial = opportunity.contact_id
            self.fields['source'].initial = opportunity.source_id
            self.fields['assigned'].initial = [
                i.id for i in opportunity.assigned.only('id')]
        else:
            del self.fields['opportunity']

        if lead:
            self.fields['client'].initial = lead.contact_id
            self.fields['source'].initial = lead.source_id
            self.fields['assigned'].initial = [
                i.id for i in lead.assigned.only('id')]

        self.fields['assigned'].help_text = ""
        self.fields['assigned'].label = _("Assigned to")
        self.fields['assigned'].widget.attrs.update({'class': 'multicomplete',
                                                     'callback': reverse('identities_ajax_user_lookup')})

        self.fields['datetime'].label = _("Date")
        self.fields['datetime'].widget.attrs.update(
            {'class': 'datetimepicker'})
        self.fields['details'].label = _("Details")

    class Meta:

        "Sale Order Form"
        model = SaleOrder
        fields = ('reference', 'client', 'opportunity', 'currency', 'source',
                  'assigned', 'status', 'datetime', 'details')


class OrderFilterForm(forms.ModelForm):

    """ Order Filters definition """

    paid = forms.ChoiceField(choices=(
        (None, '-----'), ('paid', _("Paid in full")), ('unpaid', _("Pending Payments"))), required=False)

    def __init__(self, user, skip=[], *args, **kwargs):
        super(OrderFilterForm, self).__init__(*args, **kwargs)

        if 'status' in skip:
            del self.fields['status']
        else:
            self.fields['status'].queryset = Object.filter_permitted(user,
                                                                     SaleStatus.objects.filter(use_sales=True))
            self.fields['status'].required = False
            self.fields['status'].label = _("Status")

        self.fields['paid'].label = _("Payment Status")

        self.fields['client'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['client'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['client'].required = False
        self.fields['client'].label = _("Client")

        self.fields['source'].queryset = Object.filter_permitted(
            user, SaleSource.objects.filter(active=True))
        self.fields['source'].required = False
        self.fields['source'].label = _("Source")

        self.fields['assigned'].label = _("Assigned")
        self.fields['assigned'].widget.attrs.update({'class': 'multicomplete',
                                                     'callback': reverse('identities_ajax_user_lookup')})
        if 'assigned' in skip:
            del self.fields['assigned']
        else:
            self.fields['assigned'].help_text = ""

    class Meta:

        "Order Filter Form"
        model = SaleOrder
        fields = ('client', 'source', 'assigned', 'status')


class LeadForm(forms.ModelForm):

    """ Lead form """

    def __init__(self, user, *args, **kwargs):
        super(LeadForm, self).__init__(*args, **kwargs)

        self.fields['contact'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['contact'].widget.attrs.update({'class': 'autocomplete',
                                                    'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['contact'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['contact'].label = _("Contact")

        self.fields['source'].queryset = Object.filter_permitted(
            user, SaleSource.objects.filter(active=True))
        self.fields['source'].label = _("Source")
        self.fields['products_interested'].queryset = Object.filter_permitted(
            user, Product.objects)
        self.fields['products_interested'].help_text = ""
        self.fields['products_interested'].widget.attrs.update(
            {'popuplink': reverse('sales_product_add')})
        self.fields['products_interested'].label = _("Products interested")

        self.fields['assigned'].help_text = ""
        self.fields['assigned'].label = _("Assigned to")
        self.fields['assigned'].widget.attrs.update({'class': 'multicomplete',
                                                     'callback': reverse('identities_ajax_user_lookup')})

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_order_product')[0]
            self.fields['products_interested'].initial = [long(conf.value)]
        except:
            pass

        self.fields['status'].queryset = Object.filter_permitted(
            user, SaleStatus.objects.filter(use_leads=True))
        self.fields['status'].label = _("Status")

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_lead_status')[0]
            self.fields['status'].initial = long(conf.value)
        except:
            pass

        self.fields['contact_method'].label = _("Contact method")
        self.fields['details'].label = _("Details")

    class Meta:

        "Lead Form"
        model = Lead
        fields = ('contact', 'source', 'products_interested', 'contact_method',
                  'assigned', 'status', 'details')


class LeadFilterForm(forms.ModelForm):

    """ Ticket Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(LeadFilterForm, self).__init__(*args, **kwargs)

        self.fields['contact'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['contact'].widget.attrs.update({'class': 'autocomplete',
                                                    'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['contact'].required = False
        self.fields['contact'].label = _("Contact")

        self.fields['products_interested'].queryset = Object.filter_permitted(
            user, Product.objects)
        self.fields['products_interested'].required = False
        self.fields['products_interested'].help_text = ""
        self.fields['products_interested'].label = _("Products interested")

        self.fields['source'].queryset = Object.filter_permitted(user,
                                                                 SaleSource.objects.filter(active=True))
        self.fields['source'].required = False
        self.fields['source'].label = _("Source")

        self.fields['status'].queryset = Object.filter_permitted(user,
                                                                 SaleStatus.objects.filter(use_leads=True))
        self.fields['status'].required = False
        self.fields['status'].label = _("Status")

        self.fields['contact_method'].required = False
        self.fields['contact_method'].label = _("Contact method")

    class Meta:

        "Lead Filter Form"
        model = Lead
        fields = (
            'contact', 'source', 'products_interested', 'contact_method', 'status')


class OpportunityForm(forms.ModelForm):

    """ Opportunity form """

    def __init__(self, user, lead, *args, **kwargs):
        super(OpportunityForm, self).__init__(*args, **kwargs)

        self.fields['lead'].queryset = Object.filter_permitted(
            user, Lead.objects)
        self.fields['contact'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['contact'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['contact'].widget.attrs.update({'class': 'autocomplete',
                                                    'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['products_interested'].queryset = Object.filter_permitted(
            user, Product.objects)
        self.fields['products_interested'].widget.attrs.update(
            {'popuplink': reverse('sales_product_add')})
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_order_product')[0]
            self.fields['products_interested'].initial = [long(conf.value)]
        except:
            pass
        self.fields['source'].queryset = Object.filter_permitted(user,
                                                                 SaleSource.objects.filter(active=True))
        self.fields['status'].queryset = Object.filter_permitted(user,
                                                                 SaleStatus.objects.filter(use_opportunities=True))
        self.fields['assigned'].widget.attrs.update({'class': 'multicomplete',
                                                     'callback': reverse('identities_ajax_user_lookup')})

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_opportunity_status')[0]
            self.fields['status'].initial = long(conf.value)
        except:
            pass

        if lead:
            self.fields['lead'].initial = lead.id
            self.fields['contact'].initial = lead.contact_id
            self.fields['products_interested'].initial = [
                i.id for i in lead.products_interested.only('id')]
            self.fields['source'].initial = lead.source_id
            self.fields['assigned'].initial = [
                i.id for i in lead.assigned.only('id')]
        else:
            del self.fields['lead']

        self.fields['products_interested'].help_text = ""
        self.fields['assigned'].help_text = ""

        self.fields['expected_date'].widget.attrs.update(
            {'class': 'datepicker'})
        self.fields['closed_date'].widget.attrs.update({'class': 'datepicker'})

        self.fields['contact'].label = _("Contact")
        self.fields['products_interested'].label = _("Products interested")
        self.fields['source'].label = _("Source")
        self.fields['expected_date'].label = _("Expected date")
        self.fields['closed_date'].label = _("Closed date")
        self.fields['assigned'].label = _("Assigned to")
        self.fields['amount_display'].label = _("Amount")
        self.fields['amount_currency'].label = _("Currency")
        self.fields['amount_currency'].widget.attrs.update(
            {'popuplink': reverse('finance_currency_add')})
        self.fields['amount_currency'].initial = Currency.objects.get(
            is_default=True)

        self.fields['probability'].label = _("Probability")
        self.fields['status'].label = _("Status")
        self.fields['details'].label = _("Details")

    class Meta:

        "Opportunity Form"
        model = Opportunity
        fields = ('lead', 'contact', 'products_interested', 'source',
                  'expected_date', 'closed_date', 'assigned', 'amount_currency', 'amount_display', 'probability', 'status', 'details')


class OpportunityFilterForm(forms.ModelForm):

    """ Opportunity Filters """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(OpportunityFilterForm, self).__init__(*args, **kwargs)

        self.fields['contact'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['contact'].widget.attrs.update({'class': 'autocomplete',
                                                    'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['contact'].required = False
        self.fields['contact'].label = _("Contact")

        self.fields['source'].queryset = Object.filter_permitted(user,
                                                                 SaleSource.objects.filter(active=True))
        self.fields['source'].required = False
        self.fields['source'].label = _("Source")

        self.fields['products_interested'].queryset = Object.filter_permitted(user,
                                                                              Product.objects.filter(active=True))
        self.fields['products_interested'].required = False
        self.fields['products_interested'].help_text = ""
        self.fields['products_interested'].label = _("Products interested")

        self.fields['status'].queryset = Object.filter_permitted(user,
                                                                 SaleStatus.objects.filter(use_opportunities=True))
        self.fields['status'].required = False
        self.fields['status'].label = _("Status")

    class Meta:

        "Opportunity Filter Form"
        model = Opportunity
        fields = ('contact', 'products_interested', 'source', 'status')
