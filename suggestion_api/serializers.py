from rest_framework import serializers
from suggestion_api.models import Suggestion

class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ('id', 'longtitude', 'latitude')
