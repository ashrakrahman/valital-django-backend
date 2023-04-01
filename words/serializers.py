from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator


class WordSerializer(serializers.Serializer):
    partOfSpeech = serializers.CharField()
    definitions = serializers.ListField(child=serializers.DictField())
    synonyms = serializers.ListField(child=serializers.CharField())
    antonyms = serializers.ListField(child=serializers.CharField())

    class Meta:
        fields = ["partOfSpeech", "definitions", "synonyms", "antonyms"]


class NumberSerializer(serializers.Serializer):
    num = serializers.IntegerField(
        validators=[MaxValueValidator(9), MinValueValidator(0)]
    )
