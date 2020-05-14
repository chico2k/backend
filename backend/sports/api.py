from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.permissions.permissions import IsAuthenticatedAndProfileOwner
from rest_framework.permissions import IsAuthenticated
from main.management.rest_framework.utils import inline_serializer, \
    ExceptionHandlerMixin
from .models import Sporttype
from .selectors import get_list_sport_of_profile, get_detail_sport_of_profile, \
    get_list_sporttype_to_add
from .services import add_sports_of_profile, update_sports_of_profile, \
    delete_sports_of_profile
from .constants import Success
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class SportListApi(ExceptionHandlerMixin, APIView):
    """
    List Api for Sports of Profile
    """
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        sporttype = inline_serializer(many=False, fields={
            'id': serializers.IntegerField(),
            'title': serializers.CharField()
        })
        level = serializers.IntegerField()

    def get(self, request, profile_id):
        sports = get_list_sport_of_profile(profile=profile_id)
        serializer = self.OutputSerializer(sports, many=True)
        return Response(serializer.data)


class SportDetailApi(ExceptionHandlerMixin, APIView):
    """
    Detail Api for Sports
    """
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        sporttype = inline_serializer(many=False, fields={
            'id': serializers.IntegerField(),
            'title': serializers.CharField(),
        })
        level = serializers.IntegerField()

    def get(self, request, pk, profile_id):
        sports = get_detail_sport_of_profile(id=pk)

        serializer = self.OutputSerializer(sports, many=False,)

        return Response(serializer.data)


class SportCreateApi(ExceptionHandlerMixin, APIView):
    """
    Create Api for Sports
    """
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    class InputSerializer(serializers.Serializer):
        sporttype = serializers.PrimaryKeyRelatedField(
            queryset=Sporttype.objects.all())
        level = serializers.IntegerField()

    class OutSerializer(InputSerializer):
        id = serializers.IntegerField()
        sporttype = inline_serializer(many=False, fields={
            'id': serializers.IntegerField(),
            'title': serializers.CharField()
        })

    def post(self, request, profile_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_sport = add_sports_of_profile(**serializer.validated_data,
                                          user=request.user, profile_id=profile_id)

        res = self.OutSerializer(instance=new_sport).data
        return Response(data=res, status=status.HTTP_201_CREATED)


class SportUpdateApi(ExceptionHandlerMixin, APIView):
    """
    Update Api for Sports
    """
    permission_classes = [IsAuthenticatedAndProfileOwner, ]

    class InputSerializer(serializers.Serializer):
        level = serializers.IntegerField()

    class OutSerializer(InputSerializer):
        id = serializers.IntegerField()
        sporttype = inline_serializer(many=False, fields={
            'id': serializers.IntegerField(),
            'title': serializers.CharField()
        })

    def put(self, request, profile_id, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_sport = update_sports_of_profile(
            id=pk, user=request.user, **serializer.validated_data)

        res = self.OutSerializer(instance=updated_sport).data

        return Response(data=res, status=status.HTTP_200_OK)


class SportDeleteApi(ExceptionHandlerMixin, APIView):
    """
    Delete Api for Sports
    """

    def delete(self, request, profile_id, pk):
        delete_sports_of_profile(id=pk, user=request.user)
        return Response({'message': Success.DELETED_SUCCESSFULLY}, status=status.HTTP_200_OK)


class SporttypeAvailableToAdd(ExceptionHandlerMixin, APIView):
    """
    View Api to get available Sports to add
    """
    class OutputSerializer(serializers.Serializer):
        label = serializers.CharField(source='title')
        value = serializers.IntegerField(source='id')

    def get(self, request, profile_id):
        sports = get_list_sporttype_to_add(profile=profile_id)
        serializer = self.OutputSerializer(sports, many=True)
        return Response(serializer.data)
