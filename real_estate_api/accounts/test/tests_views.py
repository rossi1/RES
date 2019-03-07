import unittest
import json

from django.shortcuts import reverse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient
from rest_framework import status

class CustomerSignUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    '''
    def test_customer_sign_up(self):
        payload = {
            'full_name': 'james okon',
            'contact_address': '5 alabded',
            'user': {
                'email': 'james@outlook.com',
                'password': '@1OBINNN',
                'contact_number': '08062156611'
            }
        }

        response = self.client.post(reverse('customer'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    '''

    def test_login_view(self):
        payload = {
            'email': 'issac_wilson@yahoo.com',
            'password': '@1OBINNN'
        }


        response = self.client.post(reverse('login'), data=payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        




if __name__ == '__main__':
    unittest.main()