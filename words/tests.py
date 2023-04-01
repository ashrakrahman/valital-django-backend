from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .views import number_to_word
from .serializers import NumberSerializer
import json


class NumberToWordTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_number_to_word_valid_data(self):
        body = {"num": 5}
        request = self.factory.post(
            "/words/number_to_word/",
            data=json.dumps(body),
            content_type="application/json",
        )
        response = number_to_word(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"data": "five"})

    def test_number_to_word_invalid_data(self):
        # create an invalid request body
        body = {"num": 543}
        request = self.factory.post(
            "/words/number-to-word/",
            data=json.dumps(body),
            content_type="application/json",
        )

        # make request to view
        response = number_to_word(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"errors": {"num": ["Ensure this value is less than or equal to 9."]}},
        )
