from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.permissions.permissions import IsAuthenticatedAndProfileOwner
from main.management.rest_framework.utils import ExceptionHandlerMixin
import requests
from location.services import add_location_of_profile
import os


class LocationGeocoderAPI(ExceptionHandlerMixin, APIView):
    """
    API to get Mapbox Information
    """
    # permission_classes = [IsAuthenticatedAndProfileOwner, ]

    class InputSerializer(serializers.Serializer):
        input = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_value = serializer.validated_data['input']
        MAPBOX_API_KEY = os.environ.get("MAPBOX_API_KEY")
        url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{input_value}.json?access_token={MAPBOX_API_KEY}'
        r = requests.get(url)
        response = r.json()
        return Response(response)


class LocationCreateApi(ExceptionHandlerMixin, APIView):
    """
    Create Api for Location
    """
    permission_classes = [IsAuthenticatedAndProfileOwner, ]

    class InputSerializer(serializers.Serializer):
        location_id = serializers.CharField()
        place_name = serializers.CharField()
        text = serializers.CharField()
        longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
        latitude = serializers.DecimalField(max_digits=9, decimal_places=6)

    class OutputSerializer(InputSerializer):
        pass

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        edit_location = add_location_of_profile(**serializer.validated_data,
                                                user=request.user)

        res = self.OutputSerializer(instance=edit_location).data

        return Response(data=res, status=status.HTTP_201_CREATED)
