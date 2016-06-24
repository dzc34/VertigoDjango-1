"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class PhoneNumberFieldAppTest(TestCase):
    def test_save_field_to_database(self):
        from vertigo.models import Adherent
        from phonenumber_field.phonenumber import PhoneNumber
        tm = Adherent()
        tm.telephone = '+41 52 424 2424'
        tm.full_clean()
        tm.save()
        pk = tm.id

        tm = Adherent.objects.get(pk=pk)
        self.assertTrue(isinstance(tm.telephone, PhoneNumber))
        self.assertEqual(str(tm.telephone), '+41524242424')

    def test_save_blank_phone_to_database(self):
        from vertigo.models import Adherent
        from phonenumber_field.phonenumber import PhoneNumber
        tm = Adherent()
        tm.save()

        pk = tm.id
        tm = Adherent.objects.get(pk=pk)
        self.assertEqual(tm.telephone, '')