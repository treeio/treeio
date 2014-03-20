# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Identities Integration library
"""
from treeio.core.models import Object, ModuleSetting
from treeio.identities.models import Contact, ContactType, ContactValue
from nuconnector import Connector, DataBlock
from django.db.models import Q
from django.db import transaction
from treeio.core.conf import settings


def _clean_missing(resource_id, items, user):
    "Clean items missing from data of their original resource"
    key = '#' + unicode(resource_id) + '.'
    contacts = Object.filter_permitted(
        user, Contact.objects).filter(nuvius_resource__contains=key)
    if not len(contacts) == len(items):
        candidates = []
        for contact in contacts:
            found = False
            for item in items:
                itemkey = key + unicode(item.id.raw)
                if itemkey in contact.nuvius_resource:
                    found = True
            if not found:
                candidates.append(contact)
        for victim in candidates:
            victim.subscribers.clear()
            victim.delete()


def _find_duplicates(resource_id, item, user):
    "Finds matching items"

    dups = []
    item_id = None
    if 'id' in item.raw:
        item_id = item.id.raw

    # Finding previously syncd items
    if item_id:
        key = '#' + unicode(resource_id) + '.' + unicode(item_id) + '#'
        dups = Object.filter_permitted(user, Contact.objects).filter(
            nuvius_resource__contains=key)
        if dups:
            return dups

    # Finding equivalent items
    # If name and (email or phone) are the same - it's same person
    if item.name:
        candidates = Object.filter_permitted(
            user, Contact.objects).filter(name=item.name.raw).distinct()
        dups = []
        if candidates and (item.email or item.phone):
            for candidate in candidates:
                matching_emails = []
                emails = candidate.contactvalue_set.filter(
                    field__field_type='email')
                if item.email.raw and emails:
                    matching_emails = emails.filter(value__in=item.email.raw)
                phones = candidate.contactvalue_set.filter(
                    field__field_type='phone')
                matching_phones = []
                if item.phone.raw and phones:
                    matching_phones = phones.filter(value__in=item.phone.raw)
                # If anything matches or if we have no emails or no phones at
                # all - add to duplicates
                if matching_emails or matching_phones or (not emails and not phones):
                    dups.append(candidate)
        elif not candidates and (item.email or item.phone):
            query = Q()
            if item.email:
                query = query & Q(contactvalue__value__in=item.email.raw)
            if item.phone:
                query = query | Q(contactvalue__value__in=item.phone.raw)
            dups = Object.filter_permitted(
                user, Contact.objects).filter(query).distinct()
        else:
            dups = candidates
    elif item.email or item.phone:
        query = Q()
        if item.email:
            query = query & Q(contactvalue__value__in=item.email.raw)
        if item.phone:
            query = query & Q(contactvalue__value__in=item.phone.raw)
        dups = Object.filter_permitted(user, Contact.objects).filter(query)

    return dups


def _get_contact_type(user):
    "Returns default contact_type for integration"
    contact_type_name = getattr(
        settings, 'HARDTREE_IDENTITIES_DEFAULT_TYPE', 'person')
    contact_type = Object.filter_permitted(
        user, ContactType.objects).filter(name__iexact=contact_type_name)
    try:
        contact_type = contact_type[0]
    except IndexError:
        contact_type = None
    return contact_type


@transaction.commit_manually
def _do_sync(data, user):
    "Run updates"

    resource_id = data.info.application.id.raw

    contact_type = _get_contact_type(user)

    for item in data.result:
        item_id = None
        if 'id' in item.raw:
            item_id = item.id.raw
        dups = _find_duplicates(resource_id, item, user)
        if dups:
            for contact in dups:
                transaction.commit()
                try:
                    fields = contact.contact_type.fields
                    contact.add_nuvius_resource(resource_id, item_id)
                    if item.name.raw:
                        contact.name = item.name.raw
                    if item.email:
                        fs = fields.filter(field_type='email')
                        if fs:
                            for iemail in item.email:
                                values = contact.contactvalue_set.filter(
                                    field__in=fs, value=iemail.raw)
                                if not values:
                                    value = ContactValue(
                                        contact=contact, field=fs[0], value=iemail.raw)
                                    value.save()
                    if item.phone:
                        fs = fields.filter(field_type='phone')
                        if fs:
                            for iphone in item.phone:
                                values = contact.contactvalue_set.filter(
                                    field__in=fs, value=iphone.raw)
                                if not values:
                                    value = ContactValue(
                                        contact=contact, field=fs[0], value=iphone.raw)
                                    value.save()

                    if item.address:
                        fs = fields.filter(name='address')
                        if fs:
                            for iaddress in item.address:
                                values = contact.contactvalue_set.filter(
                                    field__in=fs, value__icontains=iaddress.raw)
                                if not values:
                                    value = ContactValue(
                                        contact=contact, field=fs[0], value=iaddress.raw)
                                    value.save()
                    if item.website:
                        fs = fields.filter(name='website')
                        if fs:
                            for iwebsite in item.website:
                                values = contact.contactvalue_set.filter(
                                    field__in=fs, value__icontains=iwebsite.raw)
                                if not values:
                                    value = ContactValue(
                                        contact=contact, field=fs[0], value=iwebsite.raw)
                                    value.save()
                    contact.auto_notify = False
                    contact.save()
                    transaction.commit()
                except KeyboardInterrupt:
                    transaction.rollback()
                    break
                except:
                    transaction.rollback()
        else:
            if contact_type and item.name.raw:
                transaction.commit()
                try:
                    contact = Contact(contact_type=contact_type)
                    contact.add_nuvius_resource(resource_id, item_id)
                    contact.name = item.name.raw
                    contact.auto_notify = False
                    contact.set_user(user)
                    contact.save()
                    fields = contact_type.fields
                    if item.email:
                        fs = fields.filter(field_type='email')
                        if fs:
                            for iemail in item.email:
                                value = ContactValue(
                                    contact=contact, field=fs[0], value=iemail.raw)
                                value.save()
                    if item.phone:
                        fs = fields.filter(field_type='phone')
                        if fs:
                            for iphone in item.phone:
                                value = ContactValue(
                                    contact=contact, field=fs[0], value=iphone.raw)
                                value.save()
                    if item.address:
                        fs = fields.filter(name='address')
                        if fs:
                            for iaddress in item.address:
                                value = ContactValue(
                                    contact=contact, field=fs[0], value=iaddress.raw)
                                value.save()
                    if item.website:
                        fs = fields.filter(name='website')
                        if fs:
                            for iwebsite in item.website:
                                value = ContactValue(
                                    contact=contact, field=fs[0], value=iwebsite.raw)
                                value.save()
                    transaction.commit()
                except KeyboardInterrupt:
                    transaction.rollback()
                    break
                except:
                    transaction.rollback()

    _clean_missing(resource_id, data.result, user)


def sync(user=None):

    if user:
        conf = ModuleSetting.get('nuvius_profile', user=user, strict=True)
    else:
        conf = ModuleSetting.get('nuvius_profile')

    for item in conf:
        profile = item.loads()
        user = item.user
        if user:
            connector = Connector(profile_id=profile['id'])
            active_resources = ModuleSetting.get_for_module(
                'treeio.identities', 'integration_resource', user=user, strict=True)
            for resource in active_resources:
                res = resource.loads()
                response = connector.get(
                    '/service/contact-book/contact/data.json/id' + profile['id'] + '/app' + str(res.resource_id))
                data = DataBlock(response['data'])
                if data.result_name == 'success':
                    _do_sync(data, user)
