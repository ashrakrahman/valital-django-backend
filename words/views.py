from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view


@swagger_auto_schema(
    method="GET",
    security=[],
    tags=["Word API"],
    responses={"200": "Success", "400": "Bad Request"},
)
@api_view(["GET"])
def index(request):
    return JsonResponse({"Hello": "World"})
