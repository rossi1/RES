import unittest
import json

from django.shortcuts import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from ..serializer import (CustomerSerializer, AgentSerializer,
PropertyOwnerSerializer, SupplierSerializer, DeveloperSerializer,
GovernmentSerializer, HotelierSerializer, InstituteSerializer,
ValuerSerializer

)


class SerializerTestCase(TestCase):
    def setUp(self):
        self. customer_payload = {
            'full_name': 'james okon',
            'contact_address': '5 alabded',
            'contact_number': '07036690932',
            'user': {
                       'email': 'james@outlook.com',
                       'password': 'emmanuel1'
            }
       
        }

        self.payload = {'full_name': 'james okon',
        'contact_address': '42uc d',
        'contact_number': '07012374211',
        'identity': 'cct_AjMxoZH.PNG',
        'cac_number': 13821,
            'user': {
            
            'email': 'james@outlook.com',
            'password': 'emmanuel1'
       
                }
        }

        self.hotel_payload = {'hotel_name': 'as vegas',
        'hotel_website': 'https://mack.com',
        'contact_number': '09093392923',
        'cac_number': 3838383,
             'user': {
            
            'email': 'james@outlook.com',
            'password': 'emmanuel1'
            }
        }

        self.institue_payload = {
            'institute_name': 'unilag',
            'contact_number': '09093392923',
            'cac_number': 3838383,
            'website': 'https://golive.com',
            'user': {

            'email': 'james@outlook.com',
            'password': 'emmanuel1'

            }
        }


    """
    def test_customer_serializer(self):
        instance = CustomerSerializer(data=self.customer_payload)
        self.assertTrue(instance.is_valid(raise_exception=True), msg='instance is valid')
    
    def test_agent_serializer(self):
        instance = AgentSerializer(data=self.payload)
        self.assertTrue(instance.is_valid(raise_exception=True), msg='success')
    
    def test_owner_serializer(self):
        instance = PropertyOwnerSerializer(data=self.customer_payload)
        self.assertTrue(instance.is_valid(raise_exception=True), msg='success')

    def test_valuer_serializer(self):
        instance = ValuerSerializer(data=self.payload)
        self.assertTrue(instance.is_valid(raise_exception=True), msg='success')

    def test_institute_serializer(self):
        instance= InstituteSerializer(data=self.institue_payload)
        self.assertTrue(instance.is_valid(raise_exception=True), msg='success')
    
    def test_hotel_serializer(self):
        instance = HotelierSerializer(data=self.hotel_payload)
        self.assertTrue(instance.is_valid(raise_exception=True), msg='success')
    
    def test_supplier_serializer(self):
        instance = SupplierSerializer(data=self.payload)
        self.assertTrue(instance.is_valid(raise_exception=True), msg='success')

    def test_government_serializer(self):
        instance = GovernmentSerializer(data=self.payload)
        self.assertTrue(instance.is_valid(raise_exception=True), msg='success')
    
    def test_developer_serializer(self):
        instance = DeveloperSerializer(data=self.payload)
        self.assertTrue(instance.is_valid(raise_exception=True), msg='success')
    """