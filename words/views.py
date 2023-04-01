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
    return JsonResponse({"Hello": "World"})


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
            data = data[0]["meanings"]

            serializer = WordSerializer(data=data, many=True)

            if serializer.is_valid():
                serialized_data = serializer.data
                verb_exmple = None

                for wordDefinition in serialized_data:
                    if wordDefinition["partOfSpeech"] == "verb":
                        verb_exmple = wordDefinition["partOfSpeech"]
                if not verb_exmple:
                    return JsonResponse(serialized_data, safe=False)
                else:
                    return JsonResponse(verb_exmple, safe=False)
            else:
                return JsonResponse({"errors": serializer.errors}, status=400)
        elif response.status_code == 404:
            return JsonResponse(
                {"error": "Data not found"}, status=response.status_code
            )
        else:
            return JsonResponse(
                {"error": "Failed to fetch data"}, status=response.status_code
            )
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    except serializers.ValidationError as e:
        return JsonResponse({"error": "Failed to serialize data"}, status=500)


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
