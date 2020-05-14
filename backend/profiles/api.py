from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from main.management.rest_framework.utils import ExceptionHandlerMixin, \
    inline_serializer
from main.permissions.permissions import IsAuthenticatedAndProfileOwner
from profiles.selectors import get_active_profiles
from profiles.services import update_profile

from .constants import Success

from main.management.pagination.pagination import PaginationHandlerMixin

from sports.api import SportListApi


class ProfileListApi(ExceptionHandlerMixin, PaginationHandlerMixin, APIView):
    """
    List Api for Profiles
    """
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        is_guide = serializers.BooleanField()
        number_rating = serializers.IntegerField(read_only=True)
        average_rating = serializers.DecimalField(
            read_only=True, default=0, max_digits=3, decimal_places=2)
        user = inline_serializer(many=False, fields={
            'name': serializers.CharField(),
            'email': serializers.CharField()
        })

    serializer_class = OutputSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request):
        profiles = get_active_profiles()
        page = self.paginate_queryset(profiles)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)


class ProfileDetailApi(ExceptionHandlerMixin, APIView):
    """
    Detail Api for Profiles
    """
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        is_guide = serializers.BooleanField()
        number_rating = serializers.IntegerField(read_only=True)
        average_rating = serializers.DecimalField(
            read_only=True, default=0, max_digits=3, decimal_places=2)
        user = inline_serializer(many=False, fields={
            'name': serializers.CharField(),
            'email': serializers.CharField()
        })
        sport = SportListApi.OutputSerializer(many=True)
        location = inline_serializer(many=False, fields={
            'location_id': serializers.CharField(),
            'text': serializers.CharField(),
            'place_name': serializers.CharField(),
            'longitude': serializers.DecimalField(
                read_only=True, default=0, max_digits=9, decimal_places=6),
            'latitude': serializers.DecimalField(
                read_only=True, default=0, max_digits=9, decimal_places=6)
        })

    def get(self, request, profile_id):
        profiles = get_active_profiles(profile_id=profile_id)
        serializer = self.OutputSerializer(profiles, many=False)
        return Response(serializer.data)


class ProfileUpdateApi(ExceptionHandlerMixin, APIView):
    permission_classes = [IsAuthenticatedAndProfileOwner, ]

    """
    Update Api for Profiles
    """
    class InputSerializer(serializers.Serializer):
        is_guide = serializers.BooleanField()

    def put(self, request, profile_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_profile(
            profile_id=profile_id,
            user=request.user,
            **serializer.validated_data)

        return Response(
            {'message': Success.UPDATED_SUCCESSFULLY},
            status=status.HTTP_200_OK)
