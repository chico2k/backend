from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from reviews.selectors import get_list_reviews_of_profile
from reviews.services import add_review_to_profile, review_response_add
from main.management.rest_framework.utils import inline_serializer,\
    ExceptionHandlerMixin


class ReviewListApi(ExceptionHandlerMixin, APIView):
    """
    List Api for Reviews of Profile
    """
    permission_classes = [IsAuthenticated, ]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        title = serializers.CharField()
        description = serializers.CharField()
        rating = serializers.DecimalField(default=0, max_digits=2, decimal_places=1)
        author = inline_serializer(many=False, fields={
            'id': serializers.IntegerField()
        })
        is_published = serializers.BooleanField()
        created_date = serializers.DateTimeField()
        modified_date = serializers.DateTimeField()

    def get(self, request, profile_id):
        reviews = get_list_reviews_of_profile(profile=profile_id)

        serializer = self.OutputSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewCreateApi(ExceptionHandlerMixin, APIView):
    """
    Create Api for Review
    """
    permission_classes = [IsAuthenticated, ]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        rating = serializers.DecimalField(default=0, max_digits=2, decimal_places=1)

    class OutSerializer(InputSerializer):
        id = serializers.IntegerField()
        author = serializers.CharField()

    def post(self, request, profile_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_review = add_review_to_profile(**serializer.validated_data,
                                           user=request.user,
                                           profile_id=profile_id)

        res = self.OutSerializer(instance=new_review).data
        return Response(data=res, status=status.HTTP_201_CREATED)


class ReviewResponseCreateApi(ExceptionHandlerMixin, APIView):
    """
    Create Api for ReviewResponse
    """
    permission_classes = [IsAuthenticated, ]

    class InputSerializer(serializers.Serializer):
        description = serializers.CharField()

    class OutSerializer(InputSerializer):
        id = serializers.IntegerField()
        author = serializers.CharField()

    def post(self, request, profile_id, review_id):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_review_response = review_response_add(**serializer.validated_data,
                                                  user=request.user,
                                                  profile_id=profile_id,
                                                  review_id=review_id
                                                  )

        res = self.OutSerializer(instance=new_review_response).data
        return Response(data=res, status=status.HTTP_201_CREATED)
