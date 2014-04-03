# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import json
from django.test import TestCase
from treeio.identities.models import Contact, ContactType, ContactField
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object


class IdentitiesHandlersTest(TestCase):

    "Identities Handler tests"
    username = "api_test"
    password = "api_password"
    prepared = False
    authentication_headers = {"CONTENT_TYPE": "application/json",
                              "HTTP_AUTHORIZATION": "Basic YXBpX3Rlc3Q6YXBpX3Bhc3N3b3Jk"}
    content_type = 'application/json'

    def setUp(self):
        "Initial Setup"

        if not self.prepared:
            # Clean up first
            Object.objects.all().delete()

            # Create objects
            try:
                self.group = Group.objects.get(name='test')
            except Group.DoesNotExist:
                Group.objects.all().delete()
                self.group = Group(name='test')
                self.group.save()

            try:
                self.user = DjangoUser.objects.get(username=self.username)
                self.user.set_password(self.password)
                try:
                    self.profile = self.user.get_profile()
                except Exception:
                    User.objects.all().delete()
                    self.user = DjangoUser(username=self.username, password='')
                    self.user.set_password(self.password)
                    self.user.save()
            except DjangoUser.DoesNotExist:
                User.objects.all().delete()
                self.user = DjangoUser(username=self.username, password='')
                self.user.set_password(self.password)
                self.user.save()

            try:
                perspective = Perspective.objects.get(name='default')
            except Perspective.DoesNotExist:
                Perspective.objects.all().delete()
                perspective = Perspective(name='default')
                perspective.save()
            ModuleSetting.set('default_perspective', perspective.id)

            self.contact_type = ContactType(name='Person')
            self.contact_type.set_default_user()
            self.contact_type.save()

            self.contact = Contact(name='Test', contact_type=self.contact_type)
            self.contact.set_default_user()
            self.contact.save()

            self.field = ContactField(
                name='Test', label='test', field_type='text')
            self.field.set_default_user()
            self.field.save()

            self.contact_type.fields.add(self.field)

            self.client = Client()

            self.prepared = True

    def test_unauthenticated_access(self):
        "Test index page at /api/identities/fields"
        response = self.client.get('/api/identities/fields')
        # Redirects as unauthenticated
        self.assertEquals(response.status_code, 401)

    def test_get_fields_list(self):
        """ Test index page api/identities/fields """
        response = self.client.get(
            path=reverse('api_identities_types'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_field(self):
        response = self.client.get(path=reverse('api_identities_fields', kwargs={
                                   'object_ptr': self.field.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_field(self):
        updates = {'name': 'Api_update', 'required': True,
                   'label': "api label", 'field_type': 'text'}
        response = self.client.put(path=reverse('api_identities_fields', kwargs={'object_ptr': self.field.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['required'], updates['required'])
        self.assertEquals(data['label'], updates['label'])
        self.assertEquals(data['field_type'], updates['field_type'])

    def test_get_types_list(self):
        """ Test index page api/identities/types """
        response = self.client.get(
            path=reverse('api_identities_types'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_type(self):
        response = self.client.get(path=reverse('api_identities_types', kwargs={
                                   'object_ptr': self.contact_type.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_type(self):
        updates = {'name': 'Api update',
                   'details': 'Api test details', 'fields': [self.field.id]}
        response = self.client.put(path=reverse('api_identities_types', kwargs={'object_ptr': self.contact_type.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['details'], updates['details'])
        for i, field in enumerate(data['fields']):
            self.assertEquals(field['id'], updates['fields'][i])
        self.assertEquals(data['details'], updates['details'])

    def test_get_contacts_list(self):
        """ Test index page api/identities/contacts """
        response = self.client.get(
            path=reverse('api_identities_contacts'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_contact(self):
        response = self.client.get(path=reverse('api_identities_contacts', kwargs={
                                   'object_ptr': self.contact.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_contact(self):
        updates = {'name': 'Api name test', 'contact_type':
                   self.contact_type.id, 'Test___0': 'Api test details'}
        response = self.client.put(path=reverse('api_identities_contacts', kwargs={'object_ptr': self.contact.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['contact_type']['id'], updates['contact_type'])
        self.assertEquals(
            data['contactvalue_set'][0]['value'], updates['Test___0'])

    def test_update_contact_with_picture(self):
        # create field
        updates = {'name': 'picture', 'required': True,
                   'label': "Picture", 'field_type': 'picture'}
        response = self.client.post(path=reverse('api_identities_fields'), content_type=self.content_type,
                                    data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['required'], updates['required'])
        self.assertEquals(data['label'], updates['label'])
        self.assertEquals(data['field_type'], updates['field_type'])
        field_id = data['id']

        # update contact type
        updates = {'name': 'Api type', 'details': 'Api test details',
                   'fields': [field_id, self.field.id]}
        response = self.client.put(path=reverse('api_identities_types', kwargs={'object_ptr': self.contact_type.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['details'], updates['details'])
        for field in data['fields']:
            self.assertIn(field['id'], updates['fields'])
        self.assertEquals(data['details'], updates['details'])

        # update user info and upload a image
        updates = {'name': 'Test user', 'contact_type': self.contact_type.id, 'Test___0': 'Api test details',
                   'picture___0': {"type": "base64", "name": "train", "content_type": "image/jpeg",
                                   "content": "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAYEBAQFBAYFBQYJBgUGCQsIBgYICwwKCgsKCgwQDAwM\n"
                                   "DAwMEAwODxAPDgwTExQUExMcGxsbHCAgICAgICAgICD/2wBDAQcHBw0MDRgQEBgaFREVGiAgICAg\n"
                                   "ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICD/wAARCAIsApYDAREA\n"
                                   "AhEBAxEB/8QAHQABAAEFAQEBAAAAAAAAAAAAAAQBAgMFBgcICf/EAFwQAAEDAwICBgQJBgkHCQcF\n"
                                   "AAABAgMEBREGEiExBxMiQVFhCBQycRUjQlJigZGhsTNygpLB0RYkNVNzorKzwhg0NkOT0uElY2Z0\n"
                                   "g6Ol5PAmRFZ1tMPxFzdUVbX/xAAaAQEAAwEBAQAAAAAAAAAAAAAAAQIDBAUG/8QAMREBAAIBAQYD\n"
                                   "CAIBBQAAAAAAAAECAxEEEjEyQXEhgcEFEyIjM1Gx8GHRQkNygpGh/9oADAMBAAIRAxEAPwD6pAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAUyAyAyAyBTIDIDIDcA3ANwDcAyAyAyBXIDIDIDIDIDIFcgAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACmQKbgKLIBb1g\n"
                                   "FOtQCnWgU64CnXAOuQCnXIA65AHXIA61AHWoBXrAHWAN6AV3gOsArvAbwK7wK7wG4Cu4CuQK5AZA\n"
                                   "rkBkCoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABRVAsVwGJ0wG\n"
                                   "F04GNakDGtUBatWniBYtaniBataniBRa1PEC315PEB68niBX11PECvrieIFfXE8QKpVp4gXJVeYF\n"
                                   "UqfMC5KkC5KjzAu68C7rkAr1oFetAqkoF3WAXJIBckgFyPAu3gV3AVyBXIFcgVyAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACiqBjc7AEaWbAEGWqAhy12O8CLJcUTvAwO\n"
                                   "ufmBgddU8QMTrsniBjW7t8QLVu/mBZ8Lp4gV+F0X5QFyXdMcwL23ZPEC9LoniBkS5p4gZEuSY5gZ\n"
                                   "W3JPEDI24J4gZW1yL3gZW1ieIGRKrzAvSpAvSoAvSfzAvScC9JgL0lAvSUC9JAL0kAvR4FyOAu3A\n"
                                   "VyBXIFcgMgVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWOUCLNJgDWVNTg\n"
                                   "DTVVdjvA1VRcsd4GtmunmBFfdPMCK+7eYEZ15x3gR3Xrj7QGNb19IC34bXGcgG3xV7wL/hz6WQMz\n"
                                   "b35gZm3r6QGZt5+kBmbePMCQy7eYGdl18wJMd1TxAkR3NPECSy4+YGdtf5gZmV+QMza1PEDM2rQD\n"
                                   "K2p8wMragDK2cDK2YDI2UDIkoF6SAXpIBejwLkeBduAruArkCuQK5AZAqAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAMMrgNbVS4yBoa+q5gc7XVmM8QNBV3DHeBq5rj5gQZLn3ZAhyX\n"
                                   "Pn2gIUtzVO8CM+6Y+VxAwOuy59oC34WVe8CiXVfEC9t0XmrgMzbsviBIZdfFwGVt3+kBIju/D2gJ\n"
                                   "Ed37sgSY7v8ASAkR3b6QEyK74x2gJcd38wJcV2z3gSorn5gSo7ineoEqO457wJcdaniBnZWeYEll\n"
                                   "WgGdlSBnZOBlbMBlbMBkSYDIkoGRJALkeBejwLkcBduAu3AVyBXIDIFcgMgVAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAACjlAiTu4Aaatl4KBzFyqsZA5S41nMDnaqs58QNVUVfHGeAGvnrfM\n"
                                   "CDLWru4KBDkrVzzAiSVq+IGF1aBYtYviA9dUC5KxQMrK5U7wMiVygZmVy+IGZlcvjwAztuPLiBnj\n"
                                   "uC55gSo7kqLzAkR3PzAmR3XlxAlR3RfnATIrt5gTobpnvAnQXPzAmxXPPeBNhuHmBMirfMCYysTh\n"
                                   "xAkx1XHmBJZUgZ21HmBmbOBmbMBkbMBlbKBkbKBekgF6PAuR4FyPAuRwF24CuQKgVyBXIDIFQAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGN68AIFU/goHP3KfgoHIXap58QORuFTzA5ysqlA1VRU\n"
                                   "qBr56lc8wIEtSviBEkqFAwPm8wMSzAW9YA60CvXKBek6gXtnAvSoUDKlSoGRtSviBmbVqneBlZWL\n"
                                   "4gSG1nmBIjruQEiOuXvUCXHcFTvAlxXNeHECdFc18QJ9PcvMCfDc14cQNjDcuXECfDcc94E6Gu8w\n"
                                   "JkVb5gS46tPECSyqAzsqAM7ZwMzZwMzZgMjZQMiSgZEkAyJIBcjwL0eBcjgLkcBcjgLsgALgAFQA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAooGGVeAGsrH4RQOXus3MDirxU8wOPuNW1qqBz1XVIqga\n"
                                   "moqFAhS1CqBCkmAjvlAwueBbvApvAbgG4C7eBckgFySAXJIBkbMoF6TAXpOBkScDMyoAzsqwM8dU\n"
                                   "oEhlX54Alx13LiBNhuKN7wJ0Ny8wJ8NxVE5gbKnufLiBsYLj5gTobj5gT4q9FxxAmxV3mBLjrAJM\n"
                                   "dUBIZU+YEhlSBmbUIBmbOBlbMBlbKBkSUC9JAMiSAXo8C9HgXI4C9HAXIoFwACoAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAsUDBM7gBpLhJwUDkbvPhFA4W71PF3EDjrjUcVA0NVPxUDWTTKBDkkAjue\n"
                                   "BicoFiqBTIFAAACuQK5ArkC7IFyOAuRwF+4C5HgZEkAyJKBkSUDM2dQM8dR5gSGVIEuOrAmxVq+I\n"
                                   "E+Cu8wNhBX+YGwgr+XaA2EFf5gbGGv8AMCdFWp4gTI6zzAlx1YEqOq8wJDKkCQyoAztnAzNnAzNm\n"
                                   "AytlAytkAytkAyNeBkRwGRHAXooF6KBUCoFQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFFAxuUCLUOw\n"
                                   "gHPXKXgoHFXuoxuA4G71GVXiByFwqO0oGlnn4gQZZMgRpHgYlUCxVAtApkAAAAVAAVAqBcBUC7IF\n"
                                   "yKBcigXo7xAvR4F6PAytkAytlAzxzqgEplQBKZVKBMhq+HMCfDW47wJ8NcvLIGwgrwNjBXYTioE6\n"
                                   "Gu8wJsVb5gTIqzzAlx1gEqOr8wJTKkDO2pAzsnAkNnAzNmAzNlAztkAyteBma8DK1wGRFAvQC4AB\n"
                                   "UAAAAAAAAAAAAAAAAAAAAAAAAAAAACigYXqBAq3cFA5m6y8wOFvsyrnAHAXeo4uA5OulVcgaiaQC\n"
                                   "I9wGJygY1UCgFAAFAAFQAFQAFUAvQCqAVAqgF6KBVAKpzAyAXtcBeiqBka/AGZkgEhkqgSI5wJUd\n"
                                   "TxAmwVeAJ8NaBOgq1VeYE6Cs44yBPjq1XkoE2GuAmRVarwyBMirMc1AlxVfmBLjqgJMdSBJZUgSY\n"
                                   "6gCSyYCQyTIGdkgEhrwMzXAZ2qBlRQLkAqBUAAAAAAAAAAAAAAAAAAAAAAAAAAAAC1wGCRQNZWu4\n"
                                   "KByd4kVMgcFfZ/aA8+u0vacBzFXLxA1krgI7lAsVQLQKAAKAAAFQAFQKogFyIBdgCoBEAuQC7AFy\n"
                                   "IBVALwKoBegF6AZGgZWqBma8DNG8CRHMBLimAmw1CoBLiqV5gToqzzAmQ1ffkCbDWATYqsCZFVgT\n"
                                   "YqrlhQJUdWgEuGpTxAlxVAEyKYCZHKBJjkAlMeBIjcBJjcBnaBegFwBAKgAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAscBGlUDVVzuCgcheH8HAee3569oDgbtJxUDmqt3ECA9QMKqBYAAoAAoAAqAwBUC7aBe\n"
                                   "jQL0YBVGgV2oBVGeADAFcAXe4CqIBdgC5ALsAXtQC9AL2gZEwBlYBmauAJDJAJDZPACVHKoElk6g\n"
                                   "S4qgCUyoAmw1XACZFVeYEyGq8wJkVUgE2Go5cQJsVSBPhqQNhFMBNikAlxyASo3gSo3ASWKBlQC5\n"
                                   "AKgVAAAAAAAAAAAAAAAAAAAAAAAAAAABjeBGmA09evZUDjry7g4Dz2+PzuA4K7O9oDmql3ECE4DE\n"
                                   "oFAAFAADAFcAALkaBkawDI2MDK2FQL0g4gXer8QK9TxAdVgC1YwK9WBbsAqjFAuRALscAKogF6IB\n"
                                   "c1OIGRG8QMiJlQMjUwBkTxAzNAyNUDOxQM7HgSGSASI5gJUUygSopuIEuKfiBNjqOIE2Cpx3gTYq\n"
                                   "nIGyp6jkBsoJwNjDKBOikRQJsTwJcbgJUbgJDVAvQCoFQAAAAAAAAAAAAAAAAAAAAAAAAAAAY3gR\n"
                                   "Zu8DS3DkoHG3vijgPPL4q4cBwd0xlQOcqF4qBDeBiAAAAFcAV2gNigXpGBlZEoEmKnAkx0meHeBI\n"
                                   "bRqncBkSjw3IF6Ui+AFvqoFvqqrxRALfVu7AGN1PjggGN1OoBYALUjXAFUYBVGdwF23AF23hkC9u\n"
                                   "QL2oBkanegGRnhzAyoncBeiKBmagGRucAZo1QDMxeOAM7Hq0CQyTCZAkxTASYp/MCbDP3oBOgnA2\n"
                                   "NPOBtaabkBtYJcgToZAJ8EgE6J4EyNwEljgMqKBcgFwAAAAAAAAAAAAAAAAAAAAAAAAAAAMbwIsw\n"
                                   "Gmr/AGVA42894Hnl++WBwV29pQObqeYENwGMCoDAF6NAvbGBekKgZW06gZoqVV7gJkVEvgBsILcv\n"
                                   "DKAT4rUvgBLZa/IDJ8FeXACvwUvgBjW18+AGNbfj5IGB1BheQGJ1DhOQGB9GqIq4AwerL4AWOgxk\n"
                                   "C3qccwLepAdWA2AXJGBckYGRqcAL2pxAytTgBkRvDIGRnEDIBlbwAvTIGVoGVqgZ2OAkRuAlRSgS\n"
                                   "4ZcAbGmlA21NKBt6aXggGwhlA2EEnICfDIBOheBKjeBna4DIigXAVAqAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAMbwI0wGork7KgcfeWcHAeeX2P2sgcBd0XcoHN1LeKgQXgWAVRAL2tAzMiUCVHTfaBKjo1Alx\n"
                                   "W9V7gJ0FsXhwA2dNaF5qgG1prT5AbSCz+KASm2hE7gMiWpMeyBRbV3YAxOtXPgBFktWO4CM+2Y7u\n"
                                   "IEWW3qi8gI0lABEdQKi8gI7qDxAwupVAsdSeIGF1PgCnUgUSLuAqkYDq8AXtbj3qBeiKigZWoBka\n"
                                   "0DI1niBeiKBlRoFyIBkagGVigZmKBmY5UAlRPwBOp5eIG2ppQNtTSAbKCQDYQSgbCGQCdDKBNjeB\n"
                                   "IY8DMigZEUC4C5AAAAAAAAAAAAAAAAAAAAAAAAABY4CPKgGrrG8FA5O8R8HcAPP77D7XADz27xYV\n"
                                   "QOVq2rlQIDkAs2gXo0CRFCuQJ9PTLnkBsqeh3YA2sFt3Y4AbSntPkBtaa0fRA21NZvogbWmtH0QJ\n"
                                   "8dq8gJLLV5AX/BeO4Cx1sTwAwutnHkBHktnHkBDltvkBDmtyL3AQprb5AQpKDHDAEWS38+AEZ1Dj\n"
                                   "uAiyUa+AGBaPgBidSY4AY30wFnqy7uADqMKBb1QF+wC7YBkamAMrWZAyNaoF23IFzWAZEjAv28gM\n"
                                   "jWruAysRcgZ2ATIncQNnTPA21M/gBsoHgbCCQCfDIBOgkAnRPAlRuAktcBmaoF4FwFQAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAC1wGCRANfVM4KBzd2h4KBwN+gXjwA89vcC9oDgbxdbTRSOZU1LGPTnHnc79VuV\n"
                                   "A52bVtnT2esk/Nb/ALyoBgXWNvzwhlx7m/vAvZrS257UM2PJGr/iQDYUms9PqqdY+SL85mf7O4Dr\n"
                                   "LFX2m5Lijqo5nc1Yi4fj81cKB11Fbk4Ab6jtacOyBuqS0eQG3p7SidwGzgtnLgBsYrf5AS47engB\n"
                                   "mSh8gKrReQGN1F5AYn0PkBFkofICLLQoBCloU8AIMtv8gIc1B5AQpaHyAiy0PkBEdQeQEWShXwAw\n"
                                   "SUSoBgfRrnkBgdSKgGNaZQLVpkAp1KeAFEg8QLuqwBdt5AZdqgXMYBejFAyIxUAu2KBejFQC9rFA\n"
                                   "zsbyAkRoBPpwNpTqBsYXAT4XqBPheBPgeBPhcBMiUCUxQJDVAyoBcBUAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAooGF6ARJ28ANHcYMtUDib3R5RwHn98oua4A+btdW2O3anrIIm7YnK2RqKqr7bUc7n9LIGhAAA\n"
                                   "J9ntElzqOpbIkfi5UyB7NorojtFC2G8T1MtXWxPRYWpiONFwvHamXKv6WAPT6G3cuHADo6K3Jw4A\n"
                                   "byloExyA2cFB5AToqNPACXHSgZ20+AL+oAdQBasAGF9OgEaSnTwAiyU6eAESSm8gIklN5ARJKTyA\n"
                                   "hy0WeAEWSi8gIr6NqdwESSiRQIslD5AYH0ffgCNJR8wMDqXjyAwPpfLgBYtN5AWrD5AWpAoDqe4C\n"
                                   "9IwLkY1vMC9rMgXpEoGVsYFyRAXJGBejAM8bQJsIGwgAnQqBPhcBOhcBsIFA2ESgTYVAmRgSGAZk\n"
                                   "AuQCoAAAAAAAAAAAAAAAAAAAAAAABRQLHIBHlbwA1dZDlFA5e7UeUXgBw94tvtLgD5u6bLd6rqen\n"
                                   "lxhs9Mn2te5F+7AHnoAAB0eiv5Q+sD6X0hB11ta3wwv3AdpQ27GOAG9pKLlwA28FJgCfHTgSWQAZ\n"
                                   "2wgZUiAu6tACxgWOjAwvjAjviAjviAjPgAjPgAjSUwEaSlAjPpAI0lJ5AR5KPyAiyUfkBGko/ICM\n"
                                   "+iTjwAjyUQEd9F5AYXUgGJ1JgDE6lXwAs6hfACiQ8cgV6kC9IvADIkSgZGxAZEiQC9IQLkh8gMrI\n"
                                   "gJMbMAS4WgTYkUCdCgE6JAJ8CAbGECdCgEyICSwDKgFwFQAAAAAAAAAAAAAAAAAAAAAAAABYoGJy\n"
                                   "ARKiLKAaWvpdyKBy9ytu7PAD5z9Jaz9QlkrUbhN1RC9ffsc38FA8NAAAOj0V/KH1gfVXRrT9dRu4\n"
                                   "ckaB6NS0PkBtIKXHcBsIacCUyIDO2MDIjAL0aBXaBRWgWK0DE5gGFzQML4wMD4gMDoQMD4QML6cD\n"
                                   "A+nAjyU3kBgdTAYH0nkBHkpPICNJRpgCO+j8gI76PyAjvpPIDA6kVOYEd9KBidT4Ax+rgWrBx5AX\n"
                                   "NiwBkSHPcBk6vyAvSEDL1XAC5IQLkiAzsjwBJiYBLjaBMiaBNiaBsIEA2MKATokAmRoBIYgGRALk\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAACigWOQDC9mQIFRABqqqiR2eAHhPpTWTPR9BVonGkuETlX6L2SM\n"
                                   "X73IB8oAAAHR6K/lD6wPprSWuNK6P09PcdQ1iU0btjaeFEV80zkzlscacV815J3qByt59MPZM5lg\n"
                                   "04nUp7E9dN2l98USYb/tFAw2n0zL3FK34U01SzxZ7fqs8kLseKb0mTgB7r0ZdOOgdfuSltlS6kvG\n"
                                   "Fc601iJHMqJzWNUVWSJ39lc45ogHpLWAZEaBdgCuAKgUAsUDG5AMTkAxq0DG5gGJ0YGN0QGJ0IGN\n"
                                   "0AGF1OBhdTgYXUwGF9L5AYHUoEd9J5AYHUnkBgfSJ4ARn0WVAjPouIGGWjXuQCO6m8gMS068QLUg\n"
                                   "xzAvbCBkSLhxAvbEBlSJAL0jAuSJPADK2HKgZo4uIEtkYEuJgEuJigToG4A2MLQJsSAS40AkNAvA\n"
                                   "qAAAAAAAAAAAAAAAAAAAAAAAAAAAC1QMbmgYpI8gRJKbIHmPpD2Va3of1E1G9uGKKpavh1E7JHf1\n"
                                   "WqB8IAAAHR6K/lD6wOo6YnqtJp9nc1tS5Pr6r9wHmgADLSVdVR1UVVSTPp6qByPhnicrHsc3ijmu\n"
                                   "TCoqAfe3QJ0yUmu9HQPu1VTwakpJPVK2BZI2Pnc1rVbUMi4KiSI7uTG5FwNR6vgCoAABQC1QLFAx\n"
                                   "qgFitAsVALVaBarALVjAt6oCxYAMbqcDE6nAxOpgML6YDC6lAwupQML6QCO+jAjvo/ICPJSeQEZ1\n"
                                   "Hz4AYHUoGFaXyAp6sBckAF6ReQGRsIFyRAZEhAyNhAzMhUCTHGBKiiAlxRgTIYwJ0TQJcbQJcaAZ\n"
                                   "mgXgAAAAAAAAAAAAAAAAAAAAAAAAAAAAUUCmALFaBYrQOd6QbQl00LqK3bdy1dtq4Wp37nwORuOC\n"
                                   "8c+QH5rAAAHR6K/lD6wN90vPRZ7OzvbTOcqe9/8AwA8+AAAOx6MG0tRfXUU8skDpWb6eaFUa9skf\n"
                                   "gqouOyqmeXgQ+1ehLUl4rKGvsd6uHwjWW1Y5KGpkbtlko5W9lZFyu9zJGuYq+GM8ycdtYHTa56St\n"
                                   "FaHoUq9SXOOjV6KsFL7dRLj+bibl68e/GE71Lj571X6bj974tJ6dbsTPV1d0kXj4Zp4FTH+1A85u\n"
                                   "PpadNVW5VgudNb0X5NPRwORP9u2dQLKD0o+mZJV9Y1Du3c19UosfZ1OE+oD0TTXpQa3Xb66tJWov\n"
                                   "PrIti/8AdKxPuA9a0x086fum2O5U76CR3+tYvWxfXwRyfYoHpFNVUtXAyopZWzwP4skYqOav1oBe\n"
                                   "qAUwBTADaA2AOrAp1YFvVAWLCBjWADG6BAMa04GJ1OBhfTgYn0wGB1IBHkpPICPJSeQEaSj8gMC0\n"
                                   "nkBjWlwBb6v5AVSnAvSAC7qQMiQgZEhAzMhAzshAkxxASWRAS4YwJcbAJUbQJDUAyoBcAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAApgCmAKYAtdG1zVa5MtXgqL4Afl9fLctsvVwtrudFUzU655/FPVn7AI\n"
                                   "QADo9Ffyh9YG26W5FW722PubQtd+tLJ/ugcMAAAZaSpqKWpZPTyuhmYvYlauFTPDmgHpcF26UdJ0\n"
                                   "f8KI7/JE2JzKWPbO5yydfl/V4Tm3EO5fcUpMdB59fr/etQXWe7Xmslr7jUrumqJnbnL4J5InJETg\n"
                                   "ici4gAAAE2guc1K9OPZA7zT+qfZ7YHsvRz0nVVlrGKj1kopFT1mmzwcning5O5QPpmCaKogjqIXb\n"
                                   "4pWo+N6d7XJlF+wC/ADAFcAXbQK7QG0CmwC3YBasYFqxAWLEBjdCBjWADG6ADE6nAxOpgMD6UCO+\n"
                                   "l8gI76XyAwOpQMa0oFPVwLkgwBXqAL0hAvSEDIyEDOyICQyICQyMCTHGBKYwDO1oGZqAXgVAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAA57UPSFoXTm74cv1Db3t5wzTsSX6os71+pANRYOmvowv1FcLhQ36n\n"
                                   "Zb7Y9sVVWVWaSPc9FVqNWo6tXeyvJAOQ1H6WvQ/aHPjpaqqvUzeGKCBdmf6SdYGqnm3IHnt19OFM\n"
                                   "q206T4fJmqqz8Y44v8YGhl9NrXKvVYrBbGx9zXLUOX7Ue38APBNSXuW/ahud7mhZTzXSqmrJYYs9\n"
                                   "W1871kcjdyquMu4cQNcAA6PRX8ofWBO6U37tQ06Zzso4k93aev7QOOAAdHp/Srb/AGWu+DOtm1FR\n"
                                   "SRyNtzUR3X0j1SNzokRNyyRyObuT5q+SgQ9T2ajs1wS2w1iVtVTsRtxexE6plT8uKJyK7rEj9lX9\n"
                                   "65xw4qGytVruN4sj6y73pLdp6kmbBHLU9dMj6jYqpHDDGj3Oc1i5cvBERefFCNBraDTdVdr6602R\n"
                                   "7a9yuxDOqpA17Mom/wCOVu3nyXiSLo9I3mbUVZYKdsc1ZQPnZVSpI1sDG0qqksqyv2NSNu1V3LgD\n"
                                   "He9M3Ozx01RULDNRVm/1StppWTwyLGqI9EcxVw5u5MtdheKcANUAAy09VLA/cxfqA7Cxap2Y3P24\n"
                                   "55A+6+ievbcejbTla16vSahiXK8+WMfo4wB1mAK4ArgC7AFcAVwAwAwBTAFqtAtVgFOrAsWMCxYg\n"
                                   "LFiAsdCBidABhfTgYH0wGF1MBhWnAs9XAt6gCvU+QFUhAvSADI2EDMyIDOyIDOyMDOxgGdrQMqIB\n"
                                   "kQC4AAAAAAAAAAAAAAAAAAAAAAAAAANfqG6/A9guV26rr/g6lnq+p3bN/URrJt3YdjO3GcAfLet/\n"
                                   "Sb6To6SuqbelvtFvb6v8FVMUDqqWrWqZ1zdrp3IxEZDlXr1a7XYavPgHlS9JGuNS0Vwuur9R3Wtt\n"
                                   "NKsUS22kqko2zzT7la3DWrE1qMjcrndWvcnygPP611uR8zKNJJGLM5YaibDH9UirsRY2q9EcqYV3\n"
                                   "aXjwTxUIoAAAAAAAEmguFVQVDZ6d2HNVFwvFF8lA7VLr0eard1upJ67Tt2bEkbaykjbXUL9nLMDl\n"
                                   "injX3SP+oDgno1HKjV3NReDuWUAoB1+kdW0WkaVl0trUqdTzS7FWaPMNNSNVN7W7uDpKhOy5cdlm\n"
                                   "ccXcAw1l7s1mvtZNp6CjuFprkZLBBcKVJ3U+5NywfHNyjonKrFcxcOREUDprBqG7Vmj6Oi09crfa\n"
                                   "LlS3CsnuNNUyUtKx8NWkSskj9ZwxY4+re1zGrnGOCgRIaK23rpgjmsDIEs8NwpJZ5GbIadGMfElR\n"
                                   "KxjtmIlk3ORET2QJ+nqG702vNW1UlM6W5tpa6pp7K9mUr2VEu10To+Lnx9W9ZFaztLjgqcwNX0iM\n"
                                   "bHpfTCR0D7E2T1yR+n3q5dj97EWrb1uZts+NqJIvDZw4cQOAAAAGVA+19MdJqaC9GfTOp0tvwl1U\n"
                                   "cdL6p13UZzM+Pdv2S/N5bQOP/wAuP/oV/wCJ/wDlAH+XJ/0K/wDE/wDygFf8uX/oT/4n/wCUA+md\n"
                                   "PXV11s9FWyxJS1c8EUtVRI/reolexHPi34bu2OXG7CZA2QAAAAAUwAwBTAFMAU2gW7QKKwCxYwMa\n"
                                   "xAY3QgYXQAYnU4GNacCxYALepAqkIFyQgZGxAZGxAZmxgZmsAyNYBlagF6IBcgFQAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAABZLLFExZJXtjjTm9y4RPrUDQ66fHUaA1G6F7Xsfa61GvRybf83entcgPgXUmprX8\n"
                                   "F2y2UEvWVGlKnq7VUOak0VTE/wCMnlc2Tczb6zHljVbxY7C8gORul0rbnWSVlY5rppPa6uNkLEwm\n"
                                   "OzHE1jG8E7kAigAAAAAAAAAHrnRD0Et1vaJr1crg+ioEkdBTRwtR0j3MRNzlV3BrUVccsrx5d4dh\n"
                                   "0Y+jhZpOlu4ae1TJ8JWehtyXGmjY58Dqhs0vUs39W5Ht2K1+7a7njuUDYv8ARx6PZ9b6qsPXV8Ed\n"
                                   "pqKaWk6iZnZp62nSVsTutjlVdj9yI7mqY78gY630TtPOYvqN9q4X9yzxxyp/V6oDibv6Nl7t27rb\n"
                                   "rFHHuwytkhkWjazxmkh66aNffBt+kB5ff9O3Sx10tLWxLsZI+OGra1/UVDWOVvWwPe1m+N2Mtdji\n"
                                   "gGsAqx72PR7HK17eLXJwVFAvnqKiolWaokdNK72pJFVzl96rxAxgAAAD2fUvShbJegDRmgoUbPXv\n"
                                   "klqbqrV4QQxVtQ2GNfpycHrx4J+cgHmGpbdFS1kbqaPbTzQskTbxRF9lePvbkDTgXwLEk8azJuiR\n"
                                   "yLIic1bnj4dwH1hpXpg0tI9jtM6l9Vl+TZdQOfEnHkyOsXrNvhhXSJ5Aew2DpXt8zoaS/wAL7TWT\n"
                                   "YSJ021YZVX+anYropM92Fz9FAO9jkjlYj43I9i8nJxQC4AAAAAAFMAMAUwBTADaBTYBarAMaxgY1\n"
                                   "iAsWIDGsQFvVAU6oC5IgLkjAvSMDI1gGRGgXo0DIiAVAqAAAAAAAAAAAAAAAAAAAAAAAAAOf1/rC\n"
                                   "j0bo27amq29ZFbYFkbFnG+RyoyKPPdvkc1uQPlWt6L+lDpXtzNV6n1G2Caub6za7O5kjqeKKRMxo\n"
                                   "iI5EhRW+DXLjnlQPGqW/610RcbpaKSvmoJPj6C6UbH7oZEVHRSNezix3BVwuPNAObAAAAAAAAAAA\n"
                                   "AD07os6c7poS2zWp9vbdLbJIs0USyrA+ORyIjsP2yptXHLbzAjTdO+u29IDta26ZlDX9R6lHTI3r\n"
                                   "IUpc7upcj/aTd28/O4pgDWWzpa1pRa5n1m6sWoutbJuuLX8IqhnBOqcxuERqNREbj2cJgD680Lra\n"
                                   "z6y0/DebY7DXdipp3L24ZkTtRv8AdngvenEDoQNNNY5aRZZrL1MSTLuq7TUs623VXj1kPJj1/nGc\n"
                                   "fHPICHD0V9B+vevgrNLxWTUECZq6KlctJKzP+tj6hWRTRqvJ+1fNEXgBx2o/QjsUu5+m9R1NI7m2\n"
                                   "CviZUNXy6yLqFan6KgeW6j9ErpgtCOfSUtLeoW8d1DOm7H5lQkDlXybkDy++6Q1Xp9+y+Westi5w\n"
                                   "nrUEkSL7leiIv1AagAAAuiTMjfegHcVSKzRtcqfNjT7ZWIBwoAABtbPqvUdnY6K3XCWGnf8AlaRV\n"
                                   "307/AM+B+6J/6TQPRdD+klrnS0rWxqyeiz26N2eqXxwxyrs8kjVrU8APcLf6YNnrW0yJa6WkklYz\n"
                                   "rWXCtqKZd6rh/VqyiqYVYmOCvlaB1NL07agqoVqKHR3wpSIn5e2XaiqkyvLgvVqBbJ6S9loVxfNJ\n"
                                   "aktad876JkkGP6Rkv4IBPtHpOdClzVrE1AlJK7/V1cE8OPe9WdX/AFgO8smr9KX5qLZLzRXPKZxS\n"
                                   "VEUy/WjHKqfWBtwAAAAAYAAUwBRWgWqwCxWAWLGBb1YFOrAbAK7ALkaBejQLkQC7AFyAVAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAADhenDSFfq7osv9it6b6+aFk1JGny5KaVk6R+9/V7Uz3qB8y6S9JiOx6Xg\n"
                                   "s15s0011tcSUkTo3NjY/qU2NSVH9qNyIiI7CL+wDxDUF7rL7fK68VmPWa+Z88iN9lFeudrfJqcEA\n"
                                   "14AAAAAAAAAAAAAAADtOinpGrdDamjrUVz7XU4iulKny4s+21Pnx5y37O8D7VoqylrqOGspJWzUt\n"
                                   "SxssEzeLXMemWuT3ooGYDi+lPUVt03YPh6STqbtQu3WmaNyMnSV3BdmUXc1U9tqorVTgoGv0P6Y2\n"
                                   "kq+nhp9VUc1rrsI2SqhTrady/Px7bEXw4ge1ab15o3UsaSWO8U1dnj1ccidZ9ca4en2AbuWKKaN0\n"
                                   "UrGyRvTD2OTLVTwVFA4TUXQN0Rag3ur9M0kcz+c9G1aN+fHNOseV9+QPLNRehNpGp3v0/fqy2vXi\n"
                                   "2KqZHVx+5NvUPRPeqgeMaz9F3pZ03K51Nbfh6hTi2qtvxrvcsC4mz7mqnmB5fNb6633D1W4U8tJU\n"
                                   "sXtwTsdG9vva5EVAOvuuE0bUfSWLH66KBwoAAAAAVdI9+3c5XbU2tyucJ4J9oGair66hqG1FFUS0\n"
                                   "tQ32ZoXujenuc3Cgek6V9IjX1mcyOvlZe6NvOOq4TY+jO3tZ83o4D1qwa66HekbbS3S30sF3l4eq\n"
                                   "18caSOcv8zUJjdnyVHeQC++jVoasXrbRNVWWpTjH1b+uiRfHbJl/2SIBp/gT0ltC9vTmpJb7b4+V\n"
                                   "M+RJ1Rid3q9ZvxnwidkDb6c9Mq+Wyr+DtfaZWOaNcTz0SOgmb76WoXiv/aNA920N0x9HOtkayw3i\n"
                                   "KStcnG3T/EVScMqiRSYV+O9WZTzA7QAAAAAAFAKYAoqAW7QKbQG0BgBgC7AFQKgVQCoAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAPz49IrWNk1T0o3KqstNBFQ0mKRKqFiNWrkiVesqJFT2lV3ZavzUQDzMAAA\n"
                                   "AAAAAAAAAAAAAAAfR/oxdIfWUlRo64zYWla6qtb3rj4rOZYs/RVd6e9fAD1LpI6QqTRWnku0kK1f\n"
                                   "XP6qna1eCvVFVMr4cAPGtMaJ1d0sXhNR6qlfT2HdmCBMpub82NOWPMD1fUvQ3oq6WNtFT2ynp6qm\n"
                                   "b/E6hG7Vy35Mqtwrmu5L9wHDN9HG0XeiS6aQvNRZq+Nyx1Fuq13rBUR+3Gsse13BeS7eKYXvARXT\n"
                                   "0oujxO059/tcXjitbtT/AL1ifYB1GmvTHtW9KbV1jnts6cHzU3bbn+jftcn2qB7Fpbpa6PNUNb8D\n"
                                   "3ummldyp3u6qb3bH7VX6gOtR7V7wNdetNacvkXVXq10lyjxt21cMc2EXw3ouAPMdSeiv0V3aCeOg\n"
                                   "hqbEtR7aUMyrErkduRepn65jeKfI2/eoHjeqPQp1fSbpNN3qkusacUhqmupJvc3HXRqvmrmgeRao\n"
                                   "6Huk7S+51605WQQM9qqjZ6xTp75oOsjT61A44AAAAAAAD1/ou6f7vYJIbXqR77jZODW1LsvqadO7\n"
                                   "CrxkYnzV4p3eAH07brjQ3Khhr6CdlTR1Dd8M8a5a5q+CgQtQ6U05qOl9Vvdvhrovk9Y3ttz8yRMP\n"
                                   "Yvm1UA8O1v6M1TArq/RdW6RWrvbbalyNkRU4/FT8E9yPx+cBF0P6S/ShoGuSy6rhlvFDTLslpLhu\n"
                                   "ZWxJ9CdUVy+W9HJ4KgH1f0ddK+i+kC3etafrUfURtRau3S9iqgz8+Pjw+k3LfMDsAAAAAAAUApgC\n"
                                   "mAGAGAGAAFQKgVAAAAAAAAAAAAAAAAAAAAAAAAAAAB5t6QmvXaL6L7nXU8nV3Ouxb7a5OaTVCKiv\n"
                                   "TzjiR7080A/PUAAAAAAAAAAAAAAAAAAANnpi/wBXp7UFBeqT8tQzNlRvzm8nsXye1VavvA+pulS3\n"
                                   "2fVfRfVVtujar+pjuNI9iY3Iibs4T/m1UC30fL9WXTo+hp2VDVmtcjqZ0Mjc9n22dpqovysd/ID0\n"
                                   "xayrj/L0jlT58CpIn2Ltd9wGgrrnTWi/RXWCXZTXFWUt0gciscknKnqNrsLzXq3L4KngBO1P0iWf\n"
                                   "TFqkuNznRjGp8XF8qR3zWoB8/so9T9NerPhCphZb9P0zuEmxE7GfZ3cFe5QO3vvoxaTqE66wXKot\n"
                                   "dSicEf8AGxqv1bXN+8DTQ2f0kdA8bNcX3m3RcoWO9Zbj+hk7afUgG+sXpeXSgmSj1np6Snlb2ZJq\n"
                                   "bcxU98Un+8B63pXp76NtRoxtFeIoqh3/ALtVfESe7t4av1KB3sVyhkajmuRWrxRUXgBnbUxr3gct\n"
                                   "qfoq6NNUo9b3p6iqppPaqmxpDUf7eLZL/WA8i1R6Fmiq3fJp28VdolXikM6NrIU8ET8lIn1vUDyL\n"
                                   "VPokdLNmSSWghpr7TM4otFLtl2+cU3VLnybuA8cr7fXW+sloq+nkpKyB2yemnY6ORjk7nMdhUUDA\n"
                                   "AAAAPV+gjpSl0zeY7Fcpv+QLlJty7lTzv4NkRe5rlwj/ALfeH1aAA5rW/R5pjWVB6td6bM7EVKau\n"
                                   "j7M8Ofmu70+iuUA+XtVaO1v0Valp66lqpIdj91rvdLliO+i7ntdj2mLlF80A+pugL0jKHXjGWC/9\n"
                                   "XRasiZ2Fb2Ya1rU4uiT5MiJxcz628Mo0PbwAAAAAAAKYAAUAAVAAAKgAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAA+PvTW1Y6q1TZdLxP8AibbTLWVDU5ddVO2tRfNscWU/OA+bQAAAAAAAAAAAAAAAAAAAAfQ3\n"
                                   "QvqdtZon4LqXb/U3SUr2u74n9pv1YerfqA13QfeJNNa9vWnJXYiqN3Vp4vhcqov6iqB9FU11ikRM\n"
                                   "qBfc6Chu9tqKCqaj6epjdG/y3JjKeac0A+eLl0cXDUOo0nvVdsoqJy081IzOd8C7H7UXgiPVMp5K\n"
                                   "B6haHraKKKit6ReqQpiOLCxr+sm5FX6gNpFqZzfy8Mkf0kTrG/1Mr9qAbCl1DTzfkpmvXvRF4/Wg\n"
                                   "HnfSp0r6IpKZ9unoKe/XRU2tp3sR7WL5u5/UigeX6N6E73qyZ90rUbYLdL2oWtaqrx5bGKuce9QO\n"
                                   "pZoLpw0U5ZNK3t1fRt4pAyTu84Zeyv1ZA2tr9J7XFhnSj1pp9yq3g6aNrqeT37XZav1YA9Q0v6Rn\n"
                                   "RzfNrG3L1Cod/qa1Oq/rcWfeB6PR3+nqImywTNlid7MjHI5q+5U4ATo7s3xA4Ppc6JdJ9JNpc2qY\n"
                                   "2kv0LMW+8Mb8Yxe5kn85Gq82ry7sAfCeqtL3rS1+q7HeYFgr6R+16fJcnyXsXhuY5OLVA1IAAAA+\n"
                                   "1ejC+z1+kbbBdJGpeqaLqKuJXor3LCuxsnNc72ojs+YHXgANdqDT9p1BaKi03WBKiiqW4exeaL3O\n"
                                   "avc5q8UUD441xpG9dH+sPVEme18D21VquEfZc6NHZjkRU9lzVbhfBUA+2fR/6WW9Iui21FW5qaht\n"
                                   "itprvE3CbnY+LnRqcmyoi/pI5OQHpwAAAAAAAAAAwAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfn\n"
                                   "T083xb10v6prN+9sdc+kjVOW2jRKZMeXxQHBAAAAAB23RT0T6i6R7+ttteKejp0R9xucjVdFTsdn\n"
                                   "HDhue7C7WIvHyRFUzyZYpBEPrCxeiT0QW+jbFX0lReqj5dTU1M0S58m0zoWonvyefkyZbcs+C+kN\n"
                                   "Nrj0PNC3Chkk0pNLY7m1FWCKSR9TSvX5r0kV8rc8tyP4eCl8Wa9eedUTD5F1Npq86ZvtZY7zTrTX\n"
                                   "Ghf1c0a8vFHNXva5OLV70PQrbWNVWsJAAAAAAAAAB3PRXeHUVfWU+7DZo2vx5xrj/GBP1LcFtWvL\n"
                                   "df4lw2RWOkx9HsuT62ge42/USKjVR+UXiigdJQ6g5doDk9UVaU+pJ5mLiOvjjn/7RqdU/wDqsZ9o\n"
                                   "EWO7+YEqO7+YGO6yNuNuqKXcjJZmKxkyplWqvegHK6T6MbJZ6j12pnWur85ZJI1FYn6K5yoHosV5\n"
                                   "r4kRNsczU+avVr9i5T7wJcWpo0/Ko+H89OH6zct+8CVNV2u50/VVUUNZTr8iRrZG/fkDz7WfRb0W\n"
                                   "LRTXGozZdqZWaB3Zz/Ruzn3JgDyHSC67+HJodBV1Y+GJezJu6pqtT56Kuz7QPSaPp86VNMSJT6ts\n"
                                   "vrMacFmViwvX3Ob8Wv2Aeh6a9JTQV12x1NRJa6hebKlvYz5PblPtwBE6a9FWjpI0v8LWOSKqv1sY\n"
                                   "r6KaBzX9fFzdTuVvjzZ4O96gfICorVVFTCpwVFAAAAH0LTvd1UT89ra1c+eAPR3UHSppyNJJ6OWu\n"
                                   "ocbkf/nLdvjuYqvb+kBKtvSRap16uvifRS8lX22Z96dpPsA6ilrKSri62lmZNH85jkcn3AeY+kXp\n"
                                   "OK8aEfdWMzXWRyTxuTmsL1RkzfdjD/0QPNfRN1TNZul2joN+KS+wzUU7c8NzWLNEuPHfHtT84D7t\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/Lm+Vy3C9V9ert61dTLOr+PHrHq7PHj39\n"
                                   "4EIAAAAXdXJtV+1diYRXY4Jnl9uAPvj0Z9LUti6IrO6NiJVXZq3KrlTm506/F/qxIxDy7ZPeXtH2\n"
                                   "Xep4+0p7vXh4SlTH2lJjTuPlz02NL0aQ6f1RExG1Svfbap/e9mFmhz+biT7Tt2a/xbisvm6n08r7\n"
                                   "DJdpHysam7qtsDnxdlUT42ZFRI1eqqjOC5VO47VUxui5mXN1BU1Cslip2z1DYolle17p0p1ia3Ld\n"
                                   "yse7tcU5LjPDIc/VQOp6mWncqOdC90auauWqrVxlF70AxgAAAAAA2FirFpbg2TOOCooG81FWNrra\n"
                                   "12cvgduT3LwUDstJandLaabe7tsbsd+jw/ADs6DUHLtAYNWXVJIqOozxjV8Wf6REd/8AbA0kd4+k\n"
                                   "BLjvH0gJcd4+kBKju/0gJcd3+kBLju/0gMiVlM9dyoiO+e3su+1MKBp9W6cg1PSQUtRXyxRQvV+3\n"
                                   "CPznuz2VwBudOR0unqFtFQ0bWwt9p8Lk3OXxdu2/iBu/h6gqGdTU7Va72op24RfqdwUDnL10Z6Av\n"
                                   "SK91ClJM7/XUi9X/AFeLfuA46o6G9TWab1vSV/e17eLWOc6B/u3NVWr9eAPMNZaZ1Va6x1bfqR0M\n"
                                   "lZI5Vn4bJJObly3hlc5A50AAA+gLeqrQUyrxVYmZX9FAPablrfUdv6SaqGnrFfb6S2SPhoncader\n"
                                   "ti1bctTGVWVM7kXdjhnAHzT0w6+1ZVaupq2SvclT6kxsjmI1rX4llw50aJ1eccM7eSAaazdL+o7f\n"
                                   "I172tkcn+siV0En2ty3+qB6XF0u1+pdBX6nmp0lbJR1NMqy4R6PdAuHI5vBcbu9APJeim6NtfSRp\n"
                                   "2tdyjrok4eMi7E+9wH3raddQyoiPcigdNS3ajqETa9EUCaiovIAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAPysAAAAADqq58jrZNEjkWOqp4qtUc5jnM28u1hFVVVHdnmiLxzgD7J9F/V9Hfu\n"
                                   "ie20zZEWvsaLQVkOeLdir1C48HRY+tF8Dy74/d3tb7rvWs495nGTd7pUz9pWba+PWB8q+mrrCjlm\n"
                                   "sekqd6PqIFdca5E+Rub1cDV81RXrjwx4nds9PHf+6svnql1BTRWRKR8cjquGOogg4p1Csqsblc1e\n"
                                   "O5uFxjnw5Y49irLbdRUsG1rnVFN/FY6f1ulx1zXRz9b2cub2XJw5/uUNJcKllVX1NSyNIWTyvkbC\n"
                                   "3kxHuVUanLgmcAYAAAAAAAEVU4oBnZWSIxWO4tVMAbCx3V1Lujz2VXKAdbQah5doDY3K89dbl7Xs\n"
                                   "Lu/qr+8DQx3fzAlx3fzAlR3jzAlx3jzAlx3jzAlx3jzAlx3jzAlx3jzAlx3fzAlMuyKmF4oBkjq4\n"
                                   "ObMxL4xrt+5OAEqO51jPYmSRPCROP6zcfgBpOkGN1+0lWUUtOvXxJ6xSvYqPRJIuPDkvaTLeXeB8\n"
                                   "6AAAHvdl/keg/wCrxf2EA9MvX/7hV/8A8ml//wAFQPm/pXhxeKObPt0+zH5j3L/jA4gD0XQLVdo+\n"
                                   "8tTmvWon+xQDnujxGrqql3Ii4R7kymcOa3c1U80VEVAPdqDUlfSqna3IgHX2XpCVqtRz9q+Cgeg2\n"
                                   "PpBYqt3vy3vQD0hjmvYj2rlrkyi+SgVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPy+1NQO\n"
                                   "t+pLrQOTa6jrKiBU4Jjq5XN7uHcBrQAAAAA6ro46StTdH9/beLFKmXJsq6OXKwVEfzZGoqcu5U4o\n"
                                   "UyY4tHiPqbT3pldHVZSNW8UNdaaxE+MY1jamLPgyRitcv1sQ4rYL15dFtWl1z6Z9kjo5KfRlrmqa\n"
                                   "92WsrrgiRQM8Htja5z5Pc7aXps8zzmr5VvF4ud5ulTdbpUvrLhWPWWpqZVy5zl/9YRE4Ih2RGiqG\n"
                                   "SAAAAAAAAAAAAAZoauaNeCgbSO6ySUNUmfZj/FyJ+0DWNrJUAzMuT0AkR3ZfECXHd/pASo7v9ICX\n"
                                   "Hd/pAS47v9ICVHd/pAS47x9ICXHePpAS47x9ICXHePpAS47v5geDXKNkVxqoo/YZK9rPcjlRAI4A\n"
                                   "D3bTf+j1r/6pB/doB6ddJEk17VyJwR9kkdj32FQPnzpbp1bLbKjPCRs0aJ/R7F/xgefAekdHKKul\n"
                                   "rqicVV8mE/7JAOZ6PnKmrKNPnJKn/dOX9gHsQACTTXKtpl+KkX3LxQD6q0RXPrtIWeqk9uSki3e9\n"
                                   "rdufrwBvAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD88/SJsLrL0y6mgx2Kqp9fjdyRUrGJ\n"
                                   "O77HvcnvQDzgAAAAAAG5uFBQU8aYajmQSRsqHxOd1nxjFdhd6bOO1cK3l35AlQ221tuFYyVjGQNq\n"
                                   "o4IkkV6psdu3NbtXO/CJhV4eIHPSsVkj2KmFaqoqL5AWgAAAAAAAAAAAAAASo+xbZXfzsjWJ+iiu\n"
                                   "X8UAigAAAC5JHp3gZG1Uqd4GZlxkQCRHdl8QJUd38wJUd38wJcd38wJcd38wJUd38wPPq926uqHf\n"
                                   "Olev9ZQMAAD3LSaoumrbj/8Ajs/AD2L4YpotcbKq3U9TTR6d6idmFjkkYlq9Zc7rU4tlcnxW9OTO\n"
                                   "AHz70zpE616bkig6rC10U0m9XdbK10L9+F9jEcjGYTwz3geWgemdGP8Ao9cP6Z392gHJaDcjdWUC\n"
                                   "+cifbE5APZQAADRydOfSrpi6TW+13x7aCmXZBSTRwzsazCKjU6xjnIieSmM2nV6eLBS1I8HUWj0x\n"
                                   "ekGnw25Wy3V7E5ua2WCRfrR72f1B7ySdiq7O0+mjYZNqXfTVVTctzqSeOo9+EkSn/Et7xlOxT0l2\n"
                                   "tp9Kbodr8ddcai2vX5NXTS/ZmFJm/eTvwynZbu1tPSb0d3fCW7UltqJHcokqYkk/2blR/wBxbWGM\n"
                                   "4rR0dK1zXtRzVRzXJlrk4oqKSoqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPkz02tJLHcbBq2GPs\n"
                                   "TxvtlZInLfGqzQZ83NdJ+qB8vgAAAAAAzTVtVNE2KWRXxsxtRfJMJ78JwQDJHdK+OSSRsy75V3vV\n"
                                   "cL2k5O48nJngoEVVVVyvFV5qAAAAAAAAAAAAAAAAlVnxcVPT97G73/nScf7OAIoAAAAAAAAABVHv\n"
                                   "TkoGRtTKneBmZcJEAzsurk7wNfI7dI53iqqBaAA9t0WqLpa3Y/msfYqgenve5+rHPdxc7T2VXzXT\n"
                                   "wHjHTHG9NO6ckVOw6rubWr5tjolX+0gHlQHqHRR/I1X/ANY/wNA4vRLkTVNvVfnqn2sVAPaAAADy\n"
                                   "vWjNupavhhF2Kn1xt/aYX4vX2XkhpCjoAAACfbNQX61O3Wu5VVA7Oc000kK5/QVoVmsS7jT3pBdL\n"
                                   "tpqYFZqKeshY5u+CtRlSj2ouVa50qOkwvJVRyL5k78wrXZaWnTR9k9GXSTZNe6dZdLeqR1ceGXGg\n"
                                   "Vcvp5V7l5Za7GWu7/eiobUvvQ83atmthtpLri7mAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOK6Y9Ct1\n"
                                   "x0dXewtTNa+Pr7cvhVQduLj3blTYvkoH5xyRyRyOjkarJGKrXscmFRU4KioveBaAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAy0jInVDetXESdp/ubxx9fICRFRV9yfNPDHvXdl/FE5+GcAYZrfXQ/lYHtTxVq4+0DA\n"
                                   "AAAAAAAAAAAAAAAAAe06DcjtJ29U+a9PskcgHsn8Gr6ty+GfUpPgr+DPW+u8Oq2/Avq+N3Ld1vDb\n"
                                   "7XfjHEDxDpma7+BelnYXalyu6KvdlYLdj8APIQPUOij+Rqv/AKx/gaBxel/9L6P/AKx+8D2gAAA8\n"
                                   "y143GoZF+dGxfux+wwvxersnI55GOVMoiqniUdSioqc+AQoAx5hGgEpVtiSavhhVUzLvazcu1N/V\n"
                                   "u6vLuSdvHFeHiOhWbRaNPHx9HXdH+vr7ofUcV3tblR8a9XW0T1VGTR57UUifgvcvExiZrL0smOm0\n"
                                   "U0/Yl9z6G1vY9aaep73aJd0UqYngVU6yCVE7UUidzk+9OKcDurbWHyufBbFbdl0BZiAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAfE3pZdFTtN6u/hZbocWTUL1dPtTsw1/tSNX+m4yJ57vADwUAAAAAAAAAA\n"
                                   "AAAAAAAAAAAABmqYEg2MVfjdu6RPmqvJv2Ab2x3m10lG2CRXMkyrpHK3KKq+7K8gN3Dc7fN+TqGK\n"
                                   "vhnC/YvEC+Wio5+MsLJM96tRfvAgzaatUnJjol+g79+QIE2kE/1NR9T2/tT9wEGbTF1j9lrZU+i7\n"
                                   "/ewBAmoK2H8rA9ieKtXH2gYAAAAAAAAAAAB7J0eORdI0SJ8lZUX/AGrl/aB6Jbtf6yt0EdPR3aeO\n"
                                   "CFEbFFlHNa1EwiIjkVMAcN0g3ufUFRZ7bfv4xZbQk0kNDSNgolzUe1tfHEqJ2mo5ctXPHxyBza2X\n"
                                   "o3cm34IuTM/LbcolVPdmjwB0ekqfQlqppqaG61lP1r+sT1ymRzU7KJjrKd73Ly/mkA4GOxRUOqaG\n"
                                   "pgudDcKeWvRGeqSO3p289qKVsUjU89uAPVNqgMKAA846Q24vka/Op2r/AFnJ+wxycXp7HyebTU6q\n"
                                   "6kdGuG4RyxyNdhc/MVvfnuMnUkvbNHcqub2ZHq/1STdjtK7LVaq8fZzhQhJoYquKL1qWRz6nbtZD\n"
                                   "x63Y9dquVPbVGc0/cQSjsmo6a6sasbmq97fWZJnZVqP9tNrWtwqbuPPkSNhVUlJR218zWx+sW9jq\n"
                                   "CZFc1yvnkVHo9G7eOEdIn6KeRCGhtH8q0vf2l/sOLTwaV569/SW3mh9aWnRX7JUa2Nki8lTbHta/\n"
                                   "HHCK5ePd9xjE9JejekxO9Xj+XTdF/SZfOjzUiVkCOkoZdrLrbVd2Zo+aKi8U3Ii7mPT8FJraaSzz\n"
                                   "YabTT+fxL7i0xqaz6msdLerPOlRQ1bdzHfKavymPTjte1eDkO6J1fL5cU0tuzxbQlmAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAaXWeqqDSelrlqO4NfJSW2LrpI48b3cUajW7lRMqqoicQPA6r03tMNz6ppmtl+b1s\n"
                                   "8UXDz2pKBqar05JFylLo5G8eD5bhnLfzW06YX6wNTU+m5rF3+badt8XH/WPnk4fUsYGoqPTP6V5c\n"
                                   "dXRWeDGfYp51z799Q/kByWsfSK6S9X2Oosd6npJbZVIiTQNpY04tdua5HcXNc1U4KigeZAAAAAAA\n"
                                   "AAAAAAAAAAAAAAASaXqoWLUvw56Lthj+l85fJMgR3Oc5yucuXLxVVAoAAyRVNRD+SlfH+aqoBs7f\n"
                                   "e7s+qhg6/KSPazL2o7G5cZ7l+8D3ZnQbqGWijqKO60VY+RqO2bXxJx+kizfgBp67op17R87Z6w1O\n"
                                   "b6eRj0+xVY7+qBzlbarpQ59eop6VE+VNE+NPtciIBrZaKhqEzJDHJn5Soi/eBBm0zapPZY6JfoO/\n"
                                   "fkCDNpD+ZqPcj2/tT9wECbTF1j9lrZU+g7/ewBBmoK2H8rA9ieKtXH2gYAAAAAA9g6N3IulYE+bJ\n"
                                   "Ii/rZ/aB1AHKaoa5Lg12OCxphfrUDTgXwQvmmZEzi964QDkbezqdZ08bV9i4tZnySbAHtwACgHmW\n"
                                   "v66OovywM/8AdI2xuX6Tu3+DkMcnF6Wxcvm5ozdrPQRRTVkMUu7ZI5G9jiuV4J94RLaUNmpquelp\n"
                                   "c9XLXdarJVVVazq1VGphMrx2cckaqzLBdKCnjgSqpmPjh9YmpdsjkcuYtqovDHHD+PAJiWsV7lzl\n"
                                   "VXcuXea+JKWa3u23ClXOPjWp9q4/aD/KO8N8z2ofez8ITnew1SRydW9zUVyxuXh37Vy9ceXBVx9n\n"
                                   "ntx8Jefpas2vTjvTr/L0boU6Ya/QV7TrFdPp2tcnwnRJxVvck0fg9nf85OC9ypFbTSU58VNqprHN\n"
                                   "H7pL7oO18wAAAAAAAAAAAAAAAAAAAAAAQ7xZrVerbNbLtSRV1vqMdfSztR8b9rkem5q8Fw5qKB8/\n"
                                   "ek70YaDsfRTU3Ox6eorfWwVdNmqpoWRvRj37FTLccFygHxyAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAH0HoboxtVwsVNU6f15V0VwexrpqeGoarI3r8lY2qz8QOnTS/T/aF3WzU9HeoG/6usj2Kv6qO\n"
                                   "X+uBa/pA6Z7U3F+0Qy4xt9qahfnKfmJ1zgNXUdLfRdVTdVqnSdRa6lfafUUqZT60xJ9wF8NJ0AXx\n"
                                   "P4he0t0j+58zolz5Nqc/cBIl6EqCrZ1tlv8AHNGvso9Gvz+kxyJ9wGjr+hfW9MirFFDWJ3dTJx/r\n"
                                   "7AOdr9G6qoFVKq1VLMc3JGr2/rM3IBoKi3UsjlSop2q/v3N7X7wNfNpi1Sey10S/Qd/vZAgTaQ/m\n"
                                   "aj6nt/an7gIM2mbrH7LGyp9B378AQZqGsh/KwPYnirVx9oHqnRk/dplE+bPIn4L+0DsaamnqaiKm\n"
                                   "p2LJPM5I4o283OcuERPeoE/VWi7vYpoqa+0TWLM3fDlWSNVE4LhzVVMp3gaGp09QxSuiqKPqpW+1\n"
                                   "G5HMcmePLgBSmtFvppethi2vTkuVXH2qoHkEnxWunbPkXRdv1VAHtYACjnNa1XOXDU4qoHjUNHdr\n"
                                   "1Jc7tT08k0CTK+aRE4M6zKtbnxwnBOZneHbsmWtfCUN7HserHtVr28HNXgqKYvRVjkdG9r2cHNXK\n"
                                   "Lz4/WBJjuldFjq5Njmqqse3g5u72tq92SDRStuVTWKnW7Uw5z1RiI1Fe/wBpyoneuARCKSlnoG77\n"
                                   "hRt+dUQp/wB4hKtunePy3zPag97PwhOZ7KLTNVH1CZ7k++myWt0ZYuNv93pCslJA6rkVcxq5/ae1\n"
                                   "M85HIq7eGeHmN5X3Pxb1fCX6IaZrZK/TtsrZGvZJU0sMr2ScXor2Iqo5UymUzx4nfHB8nlrpaY/l\n"
                                   "siVAAAAAAAAAAAAAAAAAAAAAADyb0qIWydBuoHqvGF9E9vv9dhZ/iA+BQAHW9GnRvdukG9VVktE0\n"
                                   "UVxho5KyBs+UZKsT2NWPcnsqqP4Ljn9qBp9S6W1Fpi6SWq/2+a3V8XOGZuMp85juLXtXuc1VRQNU\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAFUbkBsUDNBTVDk6yLOWrzTmgG9tmt9e2l6JQ3mth28o1lc9n6j\n"
                                   "9zfuA6+1ekZ0nUGG1EsFwanP1iHj9sSx/gB1lH6T9BVM6m/6abIxeD3QvbJn9CRrfxAkfws9GvUS\n"
                                   "Yr7W22Syc16h0K5830/D7wM9L0UdEdzm67SerZKCpX2WU1Wxyp9S/GfeBsk6N+me0tzp/XCVzE4t\n"
                                   "jrEzw/Of14Ff4T+kRZVxcNP0l6p2+1JTKiOX7HZ/qAeRdLesNQX+50tVcLDNp6Wna5m129u/PflW\n"
                                   "R+AHFQ366xcqhXJ4Pw78eIE6HVtY38rCx6eWWr+0CdDq2hd+VifGvlhyfsAnQ3u1S+zUNT8/s/2s\n"
                                   "AdrpR8Tra9Y8K3rXcW8uSeAHonRZGyTpAszXplElc7Hm2Nzk+xUA31/qbZQT2i7ddNf9OR1NcqUd\n"
                                   "U1rHpXJxdl7URVje9WPwueCAdNBSuqukvVkdPRQ1lXmj4VLN8aUyrGlSmV4I5WLw7+HADxq5tpW3\n"
                                   "KrbScaRs0iU6r/N7l28/IDwy54i1xO5OTbhux/2uQPagAGl1jX+paarpc4e6Pqme+XscPdnIGT0Y\n"
                                   "bc64T6jgZXVFFI1lK9rqdzNrkzKipJDK2SOROKc28PrA6/UvRI/UE9xjpIKSWe3vbAtTEi0bnvdE\n"
                                   "2XCMTrYstSVPZ2JnmikTXVpjy2rweIas0Zf9MViwXWimpm82SPblip5SM3RrxXuX7ORjNHo49qrb\n"
                                   "+JaFFReRR0xKoSAZaN6MraZ6rhGzRuVfDD0UmGeTg6BnOH3s/CE5nto0f5af8xi/bTqn7C08IY4+\n"
                                   "e3f+l00m2sVmPbcuV90ilWz7+6OZet6PtMy/zlqon8efap2KehTg+P2n6lu8uiLMQAAAAAAAAAAA\n"
                                   "AAAAAAAAAADzn0iYHTdC2qmNXCpStfx8I5mPX+yB+eQAD2n0Q6nqumWmj3bfWKGrjx87DEkx/UyB\n"
                                   "9ZdL0HRc7Syv6Ro4PgVZEiiqJY5HPjleiqnVPha6VjlRq8W+4D4V6R7B0dW249ZobU/w7bJV4QT0\n"
                                   "1TBUw+TnSRRRyJ9JMe4DjgAAAAAAAAAAAAAAAAAAAAAAAABIpo8tVfMDKsQHb9G+m33OG4PVmWRr\n"
                                   "E1q+faz+wDb3jRXUVdAuz8vMsCp+dG9/4xgY59BcFXqwNPV6GcmcMA09To+dnJoGtm0/WR9ygXW7\n"
                                   "VmqrS7FBdqul2L7Ecz0bw+jnAHYWr0g+k6gwj7gyuYnyKqJq/ezq1+8CH0g9Lt61vQ01LcaOng9X\n"
                                   "dvSSDciquMd6qBwgAAAA9S6KX/8AIdUzwqVX7Y2fuA9G07eZbLfKK6xJudSStk2fOantN+tuUA3u\n"
                                   "ttS6dr6Ojtunaaemt8Ms1XN6wqblnqMZRERXdliNwnH/AIh0VJqfTly1RqJZ7mtBSXCro62jr3Mf\n"
                                   "xShfu2KnByKrV7PmgHn19rIK293Csp27IKmpmmhZ4MkkVzU+xQPB9Q7YtaVS9yVaOX63IoHtQADg\n"
                                   "uleu20VFQovGWR0r08o0wn9sDe+i7BDU6qu9M9743LQdYx8Ujo5E2TMbw2qmU7fHPAD6KpLJdLWk\n"
                                   "/wAHVbKhs8r55I6xvac9/P46PGP1FA1Ws1dXacrKW66flqZOrd6skGKhnXKm1io5nxrU49pVj5ZA\n"
                                   "+Xtd6Ek0rXsbFUMraKZMNqWcMvxlct5tXyXl9hler0Nmy6zp1cwZO8Ate5WNV6c29pPq4k14ssvL\n"
                                   "LqNrmPiY5Fa5HNRWrwXKJDwU5nuIrP8AOJv6GL+4eWngwp9S3kVKfx9q/Sd/eKVbdfL+n3j0OTJN\n"
                                   "0WaWeiquLdAzj9Buz9h34+WHye2x863d2JdzAAAAAAAAAAAAAAAAAAAAAAHFdNVP6x0SavZt34tV\n"
                                   "VJj+jiV+fq25A/OEAB6v6LVR1PTlp1NyNbMlZG7PnRTKifW5EA+v+nPRFfrXoxu9htsbZbpL1U1A\n"
                                   "17kYnWwzNfjc7CJuYjm8fED4b1B0NdKen93wppivjjZ7c8US1MKe+WDrY/vA45zXNcrXJhycFRea\n"
                                   "KBQAAAAAAAAAAAAAAAAAAAAAAAA2dCxFp08eOQNrZNO3e+3SC1Wikkra+pdthgiTKr4qvciJzVV4\n"
                                   "InMD6+0J0LLpfS9PbpcS1rszV0rfZWZ/Pb5NREanuA1UukfhjWSQUjN9Bp9H+uTp7C107NjYUX50\n"
                                   "ULnOf4bmgbOo0H2fyYGlrNB8/iwNFWaD5/FgaKt0IiIqqzCJzUD53uUkUlxqpIfyT5pHR/mq5cfc\n"
                                   "BHAAAAAAB6d0TuX4MrW9yTIv2t/4Ad0AAAAPFtXtSPWNbleHXNcq+9GqB7QBUDyDpIr/AFrU0kSL\n"
                                   "llIxsKe/23fe7AHa+i7UdV0kTMyidfbZ4+PfiSJ/D9QD6xAAcx0jaRp9UaTrresbXVaN66icqcUn\n"
                                   "j4sT3O9lfJQmJ0fG1yonUdT1fHq3tSSFXc9j+KZ5e45rRo9nFk366opDVbL+Tf7lJjizy8s9nW1i\n"
                                   "p66qo7cnW8HeP5Lic8vZpy+TXt/zqX+gj/uXk9FI+pPaPzK+r/zpq+Dl/vHFWsfv/j7e9H+TrOiD\n"
                                   "Tjtyu+Klbx+hPI3H3Hdi5Xy3tD61noRo4gAAAAAAAAAAAAAAAAAAAAADzbpt6QtD2PSV709fbolF\n"
                                   "cbxaKyOjp+rlc6TropIW7VYx7c7uHED89QAHpXo5Q1q9M2mZaanknSKod1ysa5yMY6F7XOdjkiIu\n"
                                   "eIH6EgcP0j9Mei+jyahi1I+ojW4tkdSrBCsqL1StR+cLwxvQD4H6SL9Q6g19qC92/d6jca+eople\n"
                                   "m1yxvkVWqqd2UA5wAAAAAAAAAAAAAAAAAAAAAAAAvZK9i5RQPYuir0kajQNM6lZpa31cT/ys8KrT\n"
                                   "VT/BHzqk6uRPBUA76X0wqS+TJSXClrNNWp/CeW2JFW1j0XmjZpnUzYfzkic7wwB6NpD0h/R9prbB\n"
                                   "a6C5LaaeJMRwVVNUIqq5cuc+VGyNVzl4uc5+VVcgd5bOkTovvOPg/UlqqHO5RNqoUk5Z/Jq5H/cB\n"
                                   "u3Wi31DEfHtcx3subxRQNPdbLY6WJ0tXVQUsbUy58z2xtRPFVcqIB8ydO/TFpuOmn01o6pZXzzos\n"
                                   "dwusPGGNi844Hpwe5yc3JwROXHkHzkAAAAAAABtbLqe8WZr2UMqNjkXc9jmNciqnv4gdDT9K15b/\n"
                                   "AJxSwSp9Hcxfxcn3AbWm6WaF3+c0Esfj1b2yfj1YG0pukjS03tzSQf0kbv8ABvA2tNqfT1R+SuNO\n"
                                   "q9zVkRq/Y7CgeU662rqqvVjke1yxuRzeKcYmqB7SBR72sY571w1qZcvkgHgNwqn1lfUVbvaqJHyL\n"
                                   "+kuQPQ/R2qXQdKlta1Fcs8VTHsam5V+Ic/u/MyB9dJcafO1V2uTmi8AMzaiF3JyAX7kA+aOnDRvq\n"
                                   "NTVVcEStiin6yNyIuFiqsyInDwe2Rvk1iGeSHXsl9Lafd46YvUWv9h3uJhS/CXULJ1itmxjO16p7\n"
                                   "+pMLcXq4J+COyE/hV/nQJ90X/Ef4o/1f+PqkVH+dM/Pd+MpC9un70fZno1VHW9ElrZnPUSTx+7Mi\n"
                                   "v/xnZh5XzntOPnS9RNXngAAAAAAAAAAAAAAAAAAAAAGmvui9IagngnvtlobrLTNcyB1bTxVGxr/a\n"
                                   "ROsRyccAR6bo66PqVWrS6YtMCs9hY6GmZj3YYgG0p7JZqZESnoKeFEXciRxMbx8eCIBNAAcB0t9D\n"
                                   "uk+kiiok1BU1NH8E9c+mqaV8bNqSo3rN/WskTb8Ui9wH5+6moLdbtSXW32yp9dttHWVEFFWcF66C\n"
                                   "KVzY5Mt4dtqIvADWgAAAAAAAAAAAAAAAAAABJoZLYx7vX4Jp2fJSCZsCp45V0U+fsA7LS1J0MXOe\n"
                                   "Kmv1XetPK9cLVp1FfTp5u2RQStT3McB7lavQ80LdbTHc7ZrGe40c/agqqaOF0as8ODncU7+P1Aab\n"
                                   "UvoY3SGF0um9QRVcicqWuiWBV90sayJn3sT3geC6r0ZqfSdzW26ht8tvqk4sSRMsenzo5G5Y9vm1\n"
                                   "VA0oAAAAm2293q1v32yvqaF/PdTSviX7WKgFtzvF3us/rF0rqivqF5zVMr5n/rPVVAiAAAAAAAAA\n"
                                   "AAAAAm2y2OrnSIjtvVpn7QIbmq16t8FwB9Cs4savkBp9aVi0ema16e3IzqWf9r2V+5VUDxhsKgd9\n"
                                   "0HVNZbek+zVlE1zqxiVSUzGJuc6R9JMxjUTjncrsAfWk1bNLUXue4sSO4ttUDZ417OKt1I6rciJ8\n"
                                   "5GU3JAMduu+n3OtliqGIy4O9SqJZ1XDpPWsSPiXHso2J6d4GVbhY1o4qenWf4YSiiq5URU6pySwt\n"
                                   "kTGcrze3wA5zphoaKTSNTRpVJVsc2RJHpw2T0ip17G/oux9YTWdJ1fHzmq1ytcmFTgqHK91QDpka\n"
                                   "jIKbb3wUzlz3q6KmVfvUyycZehsk/Kr2RJk+PhXPOF/3RR/vI6LT9WO0/mGeoT+Mt/Pd/alIaT0/\n"
                                   "ej649FOp67oylj3Z9XuEsfuzDC/H9c68HK+e9rR83yeyGzzAAAAAAAAAAAAAAAAAAAAAAAAAAANL\n"
                                   "rDWFg0hYKm/X6pSmoKZOK83vevsxxt+U93cn7APhbpf6ftXdIlVJTb3WzTTXfEWiFy4eicnVDkx1\n"
                                   "rvL2U7k71Dy8AAAAAAAAAAAAAAAAAAAAAAB23Rb0t6q6O7v61apllts7k+EbTIvxE7e/x2SInsvT\n"
                                   "inmnAD7p0Lrmwa207T32yTdZTy9maJ35SGZERXxSJ3Obn604pwUDJrHRWm9YWWWz3+jbVUknFjuU\n"
                                   "kT8cJIn82PTxT3LwA+F+l3olvXRzqD1KqVam1VWX2u5bdrZWJjc1ycdsjM4cn18lA4QAAAAAAAAA\n"
                                   "AAAAAAAAAMKB0GlGLvqfzW/tA1UkDlnk/OX8QPcaK+WORjWev0/WImHIsjU4pzxxwv1Ac90kTsmp\n"
                                   "KKkge2Rr3umerVRU7CbW8vzlA4dlsd4AbbT81ZZbxS3Ske6CqpX74ZmcHNfjCKgH0PoHU9vfZ6Jl\n"
                                   "/ZPXX/VlTXyUNbvVEYqQep5kTLd27dI1OC47gMsFsqlvdq1fO7baqiG1pbkTDlncltzMiceysK0y\n"
                                   "quQJdDreCe+Q2ZlJAyK02q3ddXI342SOf4Pa5JV5rsWTCAed6ruNxppap9Uispa2qroYEcvN0Umy\n"
                                   "XsrxTCqif/gDw+v41s6/84/+0c08Xt4uWOzAQ0dIx/WU1MuMYhgb+rHTt/YZZOZ27F9Kvb+0eo9q\n"
                                   "nX6D0/7iP9xHRpb6kebJWv2SI7Ge2v8AbkQhpL6o9ESbOiLxBn2Ljv29/bpoUz9ew6tn4PC9sR8y\n"
                                   "O3q92N3kAAAAAAAAAAAAAAAAAAAAcNZtUa1vst2da6e1sp7Zcqu2OjqZZ2zotLJtRZGsY9E6xm2R\n"
                                   "vi1yL3gct0idNN+0A6FNQUdI1k7tkU0Mda+Jztu7CSLG1i4TnhQOL/yxrX/NU/8As6n9wHolD0la\n"
                                   "3rqGnraeytfT1UbJoXpSXRcskbuauUgVOS9wE6h1l0hVlXHTNs8MTpVwkk9Nc4o0/Oe6BGonvA3U\n"
                                   "tT0jwxPmmjsccUbVfJI+eqRrWpxVVVY8IiIB8QdOHTHe+kS/o2WRjLJbVdHb6an3pE9c4dUKj8OV\n"
                                   "z+7KJhvcnEDzUAAAAAAAAAAAAAAAAAAAAAAAAAekdBfStU9H+r45Z3uXT9xVsF4g5ojc9idqfOiV\n"
                                   "c+aZTvA+9YpYpomSxPSSKREdHI1ctc1eKKipwVFQDmeknQNq11pKssFeiNdKm+iqsZdBUN/Jyt93\n"
                                   "JfFMoB+fN6sFyst4rLRcYuprqGV0FRH4OYuOHii80XvQCK2mcoF3qjvAAlI7PICi0rkUCx0DkAxq\n"
                                   "xQKYUAAAAAAFdqgXJGqgZmUzlAkxUDl7gOo0nbHdZUcPkt/aBgSyPdO/DflL+IGxg0+q/J+oCbBp\n"
                                   "2T2tvLmBKdZduERADrZjm0DB6tPTPZPC90Usbt8UrHK1zXJyVFTiigYl1DqWlhpYILlUNp7f1vqc\n"
                                   "PWOWOLr0Vsmxi5am5HLkDWz6w1Iye4z+tZnudMyiqpdrUcsMT4nsRuETaqLTM4oBI1r0oar1vd6G\n"
                                   "pvHUpJTxtpY2UzFjYuXq58ity7tyOdlygcxUNV88jvnOVftU5pe3j5Y7MaQKQu6C3UsvwbTvfxR6\n"
                                   "LtVePBsjI/u2GeTi7Nin5cef5kqaZc0v6f8A9O0iOEtMnPXvPqrcqZ23l8v/AO48q0mfT0fS3ohy\n"
                                   "Ys2oqfKdioppMd/biVOPl2Dp2d43tjmq+gjoeMAAAAAAAAAAAAAAAAAAAB5ro/UmlbDqPXlDdbxQ\n"
                                   "2+qfqBKhKeqqYYZFZUWyhVr9r3NXDlRyIvfhQPIvTJ1Lpy76a09FarrSXCSKtldKylnjmVqLFjLk\n"
                                   "Y52APlMD9EdCdIGkoNEaegfWuWWK2UbJGsgqH4c2BiKnZjXvA3ydIWmV9h1Y/wDMt1e/+zAoHjPp\n"
                                   "R9MlLR6G/g3Z/W4bjfl6ud9RS1NHiib+V2+sRxbusXDOHcqgfGwAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AVRMgfa3or67k1DoFbLWP31+nHNpkVebqV6KtOv6O1zPc1APaAPmL0q+j9jb1b9WUsaI24N9UuCp\n"
                                   "/PxJmJy+bo0VP0APDorI7OEaBmbYnKuETiBLTTD3UrlRvbZxVAIT7K5ytVE94GCSxSvdsa3K81A1\n"
                                   "8lpencBgda39Wq45AR1tz/ACxaB6dwFvqb/AB6o/wAubRuXuAzx29y9wE2C1uVfZA2lNZHO+SBua\n"
                                   "PTjuHZ5gdhpjTDm9a7bzRP2gS6fS3xj1Vvfz94Gzh0z2tyt7PeoEn+D2Mrj3IBGltPDb1fECDPak\n"
                                   "Z3cV55A1VfTYTCRMVPzQNU98cbHMfQU07c/6xr0X7WOYoGqqEtT/AG7OxP6GaZv9t0oGGhtmnpKp\n"
                                   "H+pVcKxosmUqI3pw5cFhYvPzEprGs6I1RZYuud6sj+p+R1mN3LjnHDmcz2YsrFY5HYwg0N51FJZH\n"
                                   "fBNAiR42sk3L45q1XJXJHi6Nkv8AD5ytnsT1bT8OSu++BEKxDXJfxjv6Sur7E/Yq7cYd/jeRovOT\n"
                                   "9/6e1+i/A6jn1BCrdvWtpXefxe9P8Ztgeb7UnXd83vm46Hjq7gK7gK5AZAqAAAAAAAAAAAAAAB5N\n"
                                   "pzS9ur+mPpSivNHT19HXxaeqIoZmJIiIymmjRcOTg5JIMoqcuC8wPJfS405X2HTGn6Rt1muFk9cl\n"
                                   "9Rpq342ppl2KuxKrO6WJGqjW9YivTHF7s8A+XwP0x6Pl/wDYHTX/AMqov/p2Ab7cB8A+kpq9+pel\n"
                                   "y8K1+6ktLktdKnglNlJftnV6geXAAAAAAAAAAAAAAAAAAAAAAAAAAgEiGPKge1ejFepLL0lU1Oq4\n"
                                   "prxDJRTZ5bsdZEvv3xo36wPs0DkulXT7L5oW5Uqt3SwsSqhXvR0C71x72oqfWB85QaQVWbscfACT\n"
                                   "DpJOtbuaBvKzRaQwJV0+FbjtoBoanS7GplG8V8gKUGlHsSTZFumk7LANHW6RdDK6ORnbReIEV2k1\n"
                                   "WF2Gd/gBD/gm7rNrmAR6nST43L2fcBFdph3NWgWrpWX2tvBQLo9MP3Y2gbGj0lJwyzh7gNxR6Qek\n"
                                   "ns4wB0FHozPHbnzA39JpPajW7c+IHVWnTjYmqm1OQEiGwsbu7PmBmS1t6pWo3mBg+CcZ7PECDUWf\n"
                                   "tL2QNXUWNVVVX6gNVWWBzs4aBqJ9LucvLAEKTSjvmgZqfSOyJVVvak/sp/xK2b4I8dUhukcp7Jno\n"
                                   "699LbpJrWou3PdyGiu+3VBpdfVImKmUbuTHhmTd+0WhpgyaRPdWbTUfVx5ZlUX/C1CsQvfJw7stR\n"
                                   "pdHxuw3v8OPNw3Uzldp0SW11vvVf2cdZBz9zm/vL44c+131rD1VJDV56qSAXJIBcjwLtwFyKBdkC\n"
                                   "oAAAAAAAAAAAAfIDfS4jteu9Q3qPSizJcoaOi6la/Yrfg59T8Zn1d2esSp5d2Oa54BxXTd6QP/6o\n"
                                   "Wu20HwD8EfB075+s9b9Z372bcY6mHH2geQAfQli9MXUlo0/bLSzT1HKtupo6VZ1llTekLUY123HZ\n"
                                   "XDePFQJi+mxqn/4bof8AbSgfOlZVz1lXPV1Dt9RUSOlmf4veu5y/WqgYgAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAABcxOIG1oINygehaIatBebdcmcJKKphnav8ARvR37APuYCyaJk0MkL+LJGqx3uVMKB49S2WS\n"
                                   "LdvjRdq4+oCUyzRPXK+wgEmpsqKxG06O6tfkqnACEtha2RvxeXOymPECRR2/1WdX9Tu4YRoEGs01\n"
                                   "HU1T5HQ7dy52gR5NKwp3Y8sAYP4I06u37Mp4YAhzaOR73IrMJ5oBFl0U3C9jlyAquj0VrcR4AzUu\n"
                                   "iWI525vPyA2dDovrJEa1mMAbOLSbY3JluccwNjS6dYnJnECc2ybcYQDZw25rU4p/6QC1be3wAtWi\n"
                                   "ZywBatubjiBgfbfogRZLNlFdjincBEfZM8m+9QMD9PpuVFTmBjj0sjnKqs4d4Gb+DbXfJ4JyKt4n\n"
                                   "RmbpvwZwI0N5kbYGsc3scVJ0N5NS0L1CJtwm5eH6pEwmllUscatTczl/wGibXXTWuJvuTmn2jQ3m\n"
                                   "w07RsguLpWfKjc37Vav7CYVyW8HSbyzBVJAL0kAyI8DI14GRHAZEUC5AKgAAAAAAAAKKBaqgflzd\n"
                                   "v5UrP6eT+2oEUAAAAAAAAAAAERV4ImVAKipwXmAAAAAAAAAAAAAAAAAAMkPMDobSxNyAej6cpGOR\n"
                                   "qeIH2VbXK6gpnLzWJir+qgEoDhpGu9Yla1jdm7n9YEplPTRpya5yrlW55IviBOnZDJD1cKJnvVAI\n"
                                   "bbai70lw7h2F8AK09AxXdr2e/AGWooYusyzvAJa2Lu5AILWxJM/JQCtTat7usxhF4KBidZY1TGMA\n"
                                   "X/AMOEw3iBljsbNq5aBJgtmzk36wMq2tiO5ZUC5KBiJwQCvqacvsAy+rIBVlGzOcAY5aRjV8MgEo\n"
                                   "UWNfndwGP1TAFrqJFRQKRWyNeYGJKCJZdnf3gX+o7VViJwAuSga1OWVCdRKXLeANVPUfaR+F+aDV\n"
                                   "a2DuX2efD/15EJiyskUaYx3g3lFgauU4DQ3l9FDtqNycUwEzLYKSoAXIBlbkDIgGVoGVoGRAKgAA\n"
                                   "AAAAAALVAxOUD8vbr/KlZ/Tyf21AigAAAAAAAAAADf6fpmRQS10ydlEw3PgnMDRzydbO+TGN7lXH\n"
                                   "vA3tXBFR2FrHNTrpcce/K8QMVio6d9HU1E7UcjeWe7CZA1VFCk1XDEvJzkRfcBKvlJDS1qRwphux\n"
                                   "Fx55UDotHWG3V9huNTUxo+aJXJE7wwzIHNWWjhrLtS0sy4imkRjl94E7V9jhs129VhVViWNr2q7n\n"
                                   "xyn7AOr1Voi0QdHts1FbGr1siRLVrlVTtphfd2wPOQAAAAAAAMkPMDoLS/CoB6Vpaoa3blfeB9lU\n"
                                   "bOqpIYl5sja3j5JgDK+RrI3PXk1Mr9QHH7pMybEzuXLl93d/+ALGRTbsJwVeaqBuIWMgpcouXeIF\n"
                                   "Yvnv4Z5ogGRkeEymMovEAqbl4Jy5gSIosMUC9kDUXh3gZXx54dyAXxwJ3/WBlSnTwAzMp02qA6lE\n"
                                   "5IA6oC1YkAokIF3VgUVnACxYNy8QKsjxwAtWECnUgV6rDQKMpmpl2OIFVi8PtAt6lQLHR4x7wKYT\n"
                                   "OXfYBgVnuz3gYpEVfZTlzAojccMY8QJFFCzc5UAl7AKdWBcjAL0YBkRoF6IBkagGRAKgAAAAAAAU\n"
                                   "UCxwGF6gfmBdf5UrP6eT+2oEUAAAAAAAAAAyU8Lp5mRN9p64A3t+mZS0cVBF4dr3IBqrRS+s18bP\n"
                                   "kou5/uQCXqSq6ysSFvsQpj61Alp/FtM/SlT+2v7gNXY25usHvX8FAyaifuuj0+ajU+7P7QOy6Pf9\n"
                                   "GLr+c/8Au0A4KgqPV66nqP5qRj/1XZA7XpTgzLb6tOUjHMVfdhU/FQOr6PFTUPRddbE/tTU3WNiR\n"
                                   "fpJ1jF/WA8YVFRVReCpzQABmo6KqraqOkpInTVMy7Y4mJlVUC2pp5qaolp527JoXKyRi9zmrhUAx\n"
                                   "gAAFzF4gba3zbXIB6f0bfx7UlrpUTKSzs3/mIu56/U1FA+uYbu13ygKXO6tZROTvl7Dfr5/cBBon\n"
                                   "OkTK8mt4IBXfuf2Wrx7wJcOHYjdxwoEpGYaiJ4gZFVGouOfeBfFlOPcBKjTMfvAMbgDO1qZAzIne\n"
                                   "BkaBlbyAooFMAU2gNoDaBXaBbgBtAbUApt7wGEAdwFigWOcBiXbniBjdjOEAxK16+w1VXvAuZDUd\n"
                                   "0aogFPUqt3NuE96ASKSjfDu3Y4+AEnYA2AEYBkRoF20CqIBeiAXAAAAAAAAAKKBjcBheB4v/AJKX\n"
                                   "RGszppqetne5yvfvqnJuVy5+QjPHuA8z9IzoV0DozQNNdtNW59PWrcooZ531E0vxD4ZlVu2R7m+2\n"
                                   "1vHGQPHejfV2k7Fc8aq01T3+1S8JFdlKiFO90Xaax3ucnuVAOz6OqLQ9/wDSRpKe3UFPU6Sq5qp9\n"
                                   "LQTwo6Hq0oJZGNdFIip2XpnC96AfW8HRx0ewIrYNL2mJq8VRlDTN4/UwD4S6XorXF0oaoitbEjoo\n"
                                   "7jUNZG3CNRyPxIjUTgjes3YTwA5AAAAAb3TdK1vWVsnssTDf2gamvqnVVU+Ze9ez7u4DdWCNtNQz\n"
                                   "1z/Pb7k/4gaF7nzTK5eL5HfeoG+1G5IqKlpk9/6qY/aBC023dc2r81qr+z9oGC9O3XSoXz/BEA7f\n"
                                   "o9/0Yuv5z/7tAPOwPQ9XZrtC22t5uj6pz1/ObtX71Ay9Bd3Sl1RNb3riO4QqiJ4vj4p9yqBy+vrT\n"
                                   "8FavudJjDOuWSP8ANk7aY92cAc+B7z0TaRp7Nol2pqpiLcbtuSlcvOOlYu3h4LI5FVfLAHlWvkhd\n"
                                   "fZJ2cHS/lE807wObAAACASqeXaqAexdCbOrr5rzL7FO1Yadf+cenaVPc3h9YHuFFqNrlzuAvZqH4\n"
                                   "Qrmqx/8AF4uyzzXvUDr7VJ2E4Y3JzAzSM2S9hctXigEiJERqbV+0CSjtzGp3gZFcir2vqwBliblO\n"
                                   "KcQJTeXAC5oGWMDOi8QL0AyIoFcgUApwArkABQABRAK7XZ5AV2OAosTgK9T5gOpaBT1eLwAJDEny\n"
                                   "UArsanJMAVwAApgBgCm0BtAqiAXIgF2AGAKgVAAAAAAAAAUUCxwGFyAYXIBEuFtobjSS0VfTR1dH\n"
                                   "O3bNTzNSSNyeDmuyigfOvSd6ItBV9bctCTpRVC5c6z1LlWBy88Qyrl0fudlPNAPnGhrNW9H+sEqY\n"
                                   "UdbNQ2aZzFR7Wv2PVqxvaqLua5HNcqeaKB9WdG/pU6Uvtsli1KjLNfaaF8u3P8VqerYrlSF7s7Hu\n"
                                   "xwY76lcoHx1XVk9dW1FbULuqKqR80zvF8jtzl+1QMAAABdFG6WRsbeLnLhAOgvMjaG2xUMftPTte\n"
                                   "7v8AtA5+ON0kjWN9py4QDf32RtLb4KFnf7XuT/iBqbTD1txgZ3bsr+jxAl6mm33DZ3RtRPrXiBfp\n"
                                   "Zua6R3zY/wAVT9wGtr3bq6oX/nHfiB3vR7/oxdfzn/3aAedgeh23+P8ARlUw83UyP/qO6xPuA4/T\n"
                                   "N0datQW+4IuPV5mOcv0c4d/VVQPQunm1tS4268xp2KuLqnu82dpv2o5QPKgPpy41sNP0e6fhgdmJ\n"
                                   "trpNq8s5gaucefMD521FU9fdJF8ANYAAAAJNvpZqupbDH3+05eTU8VA9Ot+o7dZ6KKihkRkcScvl\n"
                                   "Kveqp4qoGxg1tLVokMCuZG723d6p4e4DvNMV73JHl3ZT8QPULTcZNqcc5A6KnkjaxHO9pQJKuZt3\n"
                                   "t5Y4gXUzuC7lx4AZF3KBIicjV7TuYGXrURcIBlSRqgZGybfMDM2T6wMrN6/JUDJtk8ALkjkAqka9\n"
                                   "4FdnmARiIBXagFcJ4AVAAAAAAAAoAAAMAUwAwBXADADADAFQLgKYAqAAAAAAAAAAALVAxOQDErQL\n"
                                   "VYBTYB81VfRvZtRdPNfT3ql9atldUVPrEWXNz/FXq1Uc1Ucio5EVFRQPP+nX0cv4AUDtRWi5JVWB\n"
                                   "0zYfVanhVRPkztRFRNsreHPgvkvMDxAAAAAbrTdIiyvq5PYi9n3ga+51a1VZJL8nkz3IBM05S9bW\n"
                                   "9a72IUz9agRrzVes18jk9lvZb9QEzS8W6sfL3Rs/H/8AAGuuM3XV08ni9ce5OAG20qnaqXeCN/aB\n"
                                   "o5Xb5Xu+c5V+0D0Lo9/0Yuv5z/7tAPOwPQejR7ai13S3u5L2sf0jdv8AhA8/exzHuY7g5q4X3oB7\n"
                                   "NfP/AGl6F6Wu9uptyNc5e/MK9W9f1cqB4wB61ar7W3PQFFAkMr5qJq03ZY5dzY/YVvDjhuE96Aec\n"
                                   "1Fg1FJO9/wAGVfaVV/ISfuAs/g5qH/8Aq6v/AGEn+6BHq7ZcaNGrWUs1Mj/YWWNzM4543IgEYBwA\n"
                                   "ypVTtZ1bHbGLzRvDPv71ArC/CgdLZqxWuQD1DTFzkZswi/iB63YKmsnaxI4Xv/RUDsaakucmFWmk\n"
                                   "andlqp+IG5ZQVixI3bt8cqgF7LXVL7StAlNt7sIiyfYgGZttZ8p7l93ACTHRRN8V94GZlLAnyEAk\n"
                                   "Nii+Yn2AZEaicgLkAqAAAUAAVAAAADAACoACgDAAABUBgBgBgBgBgBgCoAAAAAAAAAAAAAAFFAtV\n"
                                   "ALFaB5h06dKd66O7VbK21Wpl1krp3wyRv39hGs3Z7GQPHP8ALC17/wDB0H21H7gOeh9I/VsWpVv6\n"
                                   "aTj9ZVzn7Pj8dtisXuzyUDQ9MfT5qfpBsdHZbnZ47TT09T632FlzI5rHRtzvxwTrFA8jAAAKsa57\n"
                                   "ka3irlwgHRXJ7bdaWUjPykiYd+0DnAOjpv8Ak+wulXhLNxT9LkBzgHQ2L+L2qpqV784/RT94HPAd\n"
                                   "Dpvs0NVJ/wCuCf8AEDngPROj3/Ri6/nP/u0A87A7Hovqdl8mg+TNCv2tVMfioGovdluDtQV8FLTS\n"
                                   "zqkzlRImOfwcu5PZRfED1fohtN4/g3d7LdqGanpqjKw9exWZ6xu1yIjseAHFr0K61Rksjm08bI8+\n"
                                   "3JxVE7+yjgORpIb2+Z1HQJUTSMVU6qn3u5c8NaB1dt6LOme5YWl07ela7gj5IZ4Wrxx7UuxAO90X\n"
                                   "6NfTjNcY6ytpo7ZDTrvxX1bXdZj5LWQOmXP521PMDa6g9HLpn1I+GGpt9DRR0znbZvWmOR27HHCb\n"
                                   "nd3gBdQ+hPrV+Frb3boUXmkfXSKn2xsT7wOkovQgoERFrdVSOX5TIqRET6nOl/YB0NH6F3RnG1PW\n"
                                   "7jdJ396skhjb9nVPX7wOjtHoq9DFv/KWqa4O+dVVMv4RLEn3AdVbeh/owtn+Z6aoU/pYuu/vd4G8\n"
                                   "p7BY6L/M7fTU2P5mGOP+yiAZpGgYlaBbtAqjAL0YBkawDI1gGRGgZEQCuALgAAAAwAwAAYArgAAA\n"
                                   "YAYAYAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAApgBgCmAGAK4A8q6augCzdJnU1zq+W23yjh6ikqE+\n"
                                   "MgVm5X7ZIeHe5e01UX38gPjvpF6F+kDQM7vhu3q+3ZxHdqXMtI/PLt4RWKvg9EUDhgAG405RpLUr\n"
                                   "UP8AycPL3gRLvWrV1r3/ACG9lnuQDFQUy1NXHD85ePu7wNpqapTrI6RnsxplU8+4DRgdLJDKzTsU\n"
                                   "ELHPkmx2WIqr2u0vICJR6K1bWLintFUue90bmJ9r9qAdpYuivWS2meGWmZTSy7tvWyN70wnsbwM9\n"
                                   "F6P96kx63c4IV+bGx0v49WB6HpLoXdb7dPQxuq671lVV7o4lTm3bwwjgNvavRityKi/AMsjk+VVT\n"
                                   "K1PrarkT7gO0s3o/toXpLTUFuoZE+WiZf9rWL+IHT0fQ8zG6qr0a7vbBEn9py/sA3FN0V6ai/Kuq\n"
                                   "J/J0iNT+ojQNpT6G0lB7Nsif/S5l/vFcBuKalpqWJIaaJkETeUcbUa1PqTCAZQAAAAAAAKKBjcgG\n"
                                   "J7AMSsAt2AXJGBekYGRGAXo0C5GgVwBXAFcAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAMc8EFRBJBURtmglarJYnojmua7grXNXgqKgHg3SZ6IujdQdZX6UemnLo7KrTNarq\n"
                                   "GR39Hzh/Q4J80D5V130V660NWpTaitklPG9+ynrmfGUsq93VzN7OVTjtXDvFAN/Q9HOrn2VkVHR7\n"
                                   "XTJxle9rU7XNeefuAuougPU8q/xqspqdPo75F+zDfxA63T/QJHRy9ZUV01RK5NrUii2fjvA6yj9G\n"
                                   "aiqJllmtVZUveuVdO90afdsQDrrT6NtBDjFnoIMcnzYld9vbUDsKHoYjiajZauKJqcmwxfv2gbqm\n"
                                   "6KbBGnx008y+SoxPsRFA2tPoLSkOMUDZFTvkVzvxXAG1p7RaqfHUUcMWOStjai/gBLAAAAAAAAAA\n"
                                   "AAAAAAAKKgFitAsVgFNgF2wC5GgXbQK4AqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAi3O2UF0oJqC4U7KqjqGqyaCVqPY5F8UdlANDQ9G2kaNiMZSLIxvBiSPcuETw\n"
                                   "4oBuKfT9jp0xFQQNx37EVftXKgT2sYxNrERqeCcAKgAAAAAAAAAAAAAAAAAAAAAAAACmAKYAYArg\n"
                                   "CuAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB\n"
                                   "/9k="}}
        response = self.client.put(path=reverse('api_identities_contacts', kwargs={'object_ptr': self.contact.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['contact_type']['id'], updates['contact_type'])
        for value in data['contactvalue_set']:
            if value['name'] == 'Test':
                self.assertEquals(value['value'], updates['Test___0'])
            elif value['name'] == 'picture':
                self.assertTrue(
                    value['value'].endswith(updates['picture___0']['name']))
