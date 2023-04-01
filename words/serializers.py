from rest_framework import serializers


class WordSerializer(serializers.Serializer):
    partOfSpeech = serializers.CharField()
    definitions = serializers.ListField(child=serializers.DictField())
    synonyms = serializers.ListField(child=serializers.CharField())
    antonyms = serializers.ListField(child=serializers.CharField())

    class Meta:
        fields = ["partOfSpeech", "definitions", "synonyms", "antonyms"]
