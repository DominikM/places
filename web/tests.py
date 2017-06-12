from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
import json

# Create your tests here.

class WebTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'ben_bitdiddle',
            'ben@gmail.com',
            '123abc'
        )

    def test_create_place(self):
        self.client.login(username='ben_bitdiddle', password='123abc')
        response = self.client.post('/create/place/', {
            'name': 'Happy House',
            'address': '123 Happy Lane',
            'lat': 37.7749,
            'lng': 122.4194,
            'notes': 'I love this place!',
            'place_id': '123abc',
            'date': '2017-06-08',
            'checkin_notes': 'Good visit!'
        })
        print(response.json()['place']['fields'])
        self.assertEqual(response.json()['status'], 'OK')
        self.assertDictEqual(response.json()['place']['fields'],
                         {
                             'name': 'Happy House',
                             'address': '123 Happy Lane',
                             'lat': 37.7749,
                             'lng': 122.4194,
                             'notes': 'I love this place!',
                             'place_id': '123abc',
                             'user': self.user.id,
                             'togo': False,
                             'id': 1
                         })