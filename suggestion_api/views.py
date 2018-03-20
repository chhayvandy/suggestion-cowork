from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from suggestion_api.models import Suggestion
from suggestion_api.serializers import SuggestionSerializer
from suggestion_api.getDataFromMlab import getUserLocation
import json
@api_view(['GET', 'POST'])
def suggestion_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Suggestion.objects.all()
        serializer = SuggestionSerializer(snippets, many=True)
        resultData = { "success": True,
                       "data" : serializer.data}
        return Response(resultData)
    elif request.method == 'POST':
        serializer = SuggestionSerializer(data=request.data)
        if serializer.is_valid():
            print(type(serializer.data))
            if not serializer.data:
                print("data Null")
            else:
                result = getUserLocation.getCoworkingForRecommendation(serializer.data)
                resultRecomment = json.loads(result)
                resultData = { "success": True,
                                "data" : resultRecomment}
            return Response(resultData, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)