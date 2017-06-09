from django.test import TestCase
from django.test.client import Client

# Create your tests here.

class WebTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_place(self):
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
        print(response.json()['place'])
        self.assertEqual(response.json()['status'], 'OK')
        self.assertJSONEqual(response.json()['place'],
                         {
                             'name': 'Happy House',
                             'address': '123 Happy Lane',
                             'lat': 37.7749,
                             'lng': 122.4194,
                             'notes': 'I love this place!',
                             'place_id': '123abc',
                         })