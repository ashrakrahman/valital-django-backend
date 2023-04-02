import json
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
import requests
from rest_framework.decorators import api_view
from rest_framework import serializers
from .serializers import NumberSerializer, WordSerializer
from drf_yasg import openapi


@swagger_auto_schema(
    method="GET",
    security=[],
    tags=["Word API"],
    responses={"200": "Success", "400": "Bad Request"},
)
@api_view(["GET"])
def index(request):
    return JsonResponse(
        {
            "app": "Valital django Backend",
            "version": "0.0.1",
            "developer_name": "Ashrak Rahman Lipu",
            "developer_email": "ashrakrahman@gmail.com",
            "developer_contact": "+14384622346",
            "developer_address": "Montreal,Quebec",
        }
    )


@swagger_auto_schema(
    method="GET",
    security=[],
    tags=["Word API"],
    responses={"200": "Success", "400": "Bad Request"},
)
@api_view(["GET"])
def get_word(request, word):
    try:
        response = requests.get(
            "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
        )
        if response.status_code == 200:
            data = response.json()
            verb_data = None

            for element in data:
                for meaning in element["meanings"]:
                    if meaning["partOfSpeech"] == "verb":
                        verb_data = meaning
                        break

            if verb_data is None:
                return JsonResponse(
                    {"data": data},
                    safe=False,
                )

            serializer = WordSerializer(data=verb_data)

            if serializer.is_valid():
                serialized_data = serializer.data
                for wordDefinition in serialized_data["definitions"]:
                    if "example" in wordDefinition and verb_data is not None:
                        verb_exmple = wordDefinition["example"]
                        return JsonResponse(
                            {
                                "data": {
                                    "partOfSpeech": serialized_data["partOfSpeech"],
                                    "example": verb_exmple,
                                }
                            },
                            safe=False,
                        )
                    else:
                        return JsonResponse(
                            {"error": "Data not found"}, status=response.status_code
                        )
            else:
                return JsonResponse({"errors": serializer.errors}, status=400)
        else:
            return JsonResponse(
                {"error": "Failed to fetch data"}, status=response.status_code
            )
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


@swagger_auto_schema(
    method="POST",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "num": openapi.Schema(type=openapi.TYPE_NUMBER),
        },
    ),
    security=[],
    tags=["Word API"],
    responses={"200": "Success", "400": "Bad Request"},
)
@api_view(["POST"])
def number_to_word(request):
    body_unicode = request.body.decode("utf-8")
    body_data = json.loads(body_unicode)

    serializer = NumberSerializer(data=body_data)
    digit_to_str = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }

    if serializer.is_valid():
        num = serializer.validated_data["num"]
        return JsonResponse({"data": digit_to_str[num]})
    else:
        return JsonResponse({"errors": serializer.errors}, status=400)
