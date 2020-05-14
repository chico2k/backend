from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.permissions.permissions import IsAuthenticatedAndProfileOwner
from main.management.rest_framework.utils import ExceptionHandlerMixin
from experiences.selectors import \
    get_list_experience_of_profile, \
    get_detail_experience_of_profile
from experiences.services import \
    add_experience, \
    update_experience, \
    delete_experience
from main.messages.messages import Success


class ExperienceListApi(ExceptionHandlerMixin, APIView):
    """
    List Api for Experiences of Profile
    """
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        title = serializers.CharField()
        description = serializers.CharField()
        from_date = serializers.DateField()
        to_date = serializers.DateField()
        is_current = serializers.BooleanField()

    def get(self, request, profile_id):
        experiences = get_list_experience_of_profile(profile=profile_id)
        serializer = self.OutputSerializer(experiences, many=True)
        return Response(serializer.data)


class ExperienceDetailApi(ExceptionHandlerMixin, APIView):
    """
    Detail Api for Experience
    """
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        title = serializers.CharField()
        description = serializers.CharField()
        from_date = serializers.DateField()
        to_date = serializers.DateField()
        is_current = serializers.BooleanField()

    def get(self, request, pk, profile_id):
        experience = get_detail_experience_of_profile(id=pk)

        serializer = self.OutputSerializer(experience, many=False,)

        return Response(serializer.data)


class ExperienceCreateApi(ExceptionHandlerMixin, APIView):
    """
    Create Api for Experiences
    """
    permission_classes = [IsAuthenticatedAndProfileOwner, ]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        from_date = serializers.DateField()
        to_date = serializers.DateField()
        is_current = serializers.BooleanField()

    class OutputSerializer(InputSerializer):
        id = serializers.IntegerField()

    def post(self, request, profile_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_experience = add_experience(
            **serializer.validated_data,
            user=request.user,
            profile_id=profile_id)

        res = self.OutputSerializer(instance=new_experience).data
        return Response(data=res, status=status.HTTP_201_CREATED)


class ExperienceUpdateApi(ExceptionHandlerMixin, APIView):
    """
    Update Api for Experience
    """
    permission_classes = [IsAuthenticatedAndProfileOwner, ]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        from_date = serializers.DateField()
        to_date = serializers.DateField()
        is_current = serializers.BooleanField()

    def put(self, request, profile_id, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_experience(
            id=pk,
            profile_id=profile_id,
            user=request.user,
            **serializer.validated_data)

        return Response(
            {'message': Success.UPDATED_SUCCESSFULLY},
            status=status.HTTP_200_OK
        )


class ExperienceDeleteApi(ExceptionHandlerMixin, APIView):
    """
    Delete Api for Experience
    """

    def delete(self, request, profile_id, pk):
        delete_experience(
            id=pk,
            user=request.user)

        return Response(
            {'message': Success.DELETED_SUCCESSFULLY},
            status=status.HTTP_200_OK)
