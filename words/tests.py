from django.test import TestCase
import requests
from rest_framework.test import APIRequestFactory
from .views import number_to_word, get_word, index
import json
from django.urls import reverse
from unittest.mock import patch


class GetWordTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse("get-word", args=["walk"])
        # Load the mock data from the JSON file
        with open("words/fixtures/mock_data.json") as f:
            self.mock_data = json.load(f)
        with open("words/fixtures/mock_data_non_verb.json") as f:
            self.mock_data_non_verb = json.load(f)

    @patch("requests.get")
    def test_get_word_returns_correct_response_of_verb_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_data
        request = self.factory.get(self.url, {"word": "walk"})
        response = get_word(request, "walk")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "data": {
                    "partOfSpeech": "verb",
                    "example": "To walk briskly for an hour every day is to keep fit.",
                }
            },
        )

    @patch("requests.get")
    def test_get_word_returns_correct_response_of_non_verb_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_data_non_verb
        request = self.factory.get(self.url, {"word": "banana"})
        response = get_word(request, "banana")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"data": self.mock_data_non_verb},
        )

    @patch("requests.get")
    def test_get_word_returns_error_on_failed_request(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")
        request = self.factory.get(self.url, {"word": "walk"})
        response = get_word(request, "walk")
        self.assertEqual(response.status_code, 500)


class NumberToWordTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse("number-to-word")

    def test_number_to_word_valid_data(self):
        body = {"num": 5}
        request = self.factory.post(
            self.url,
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
            self.url,
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


class WhoMadeMeTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse("index")

    def test_who_made_me_valid_data(self):
        request = self.factory.get(
            self.url,
            content_type="application/json",
        )
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "app": "Valital django Backend",
                "version": "0.0.1",
                "developer_name": "Ashrak Rahman Lipu",
                "developer_email": "ashrakrahman@gmail.com",
                "developer_contact": "+14384622346",
                "developer_address": "Montreal,Quebec",
            },
        )
