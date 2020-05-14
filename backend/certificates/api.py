from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.permissions.permissions import IsAuthenticatedAndProfileOwner
from main.management.rest_framework.utils import ExceptionHandlerMixin
from certificates.selectors import \
    get_detail_certificate, \
    get_list_certificate

from certificates.services import \
    add_certificate, \
    update_certificate,\
    delete_certificate
from main.messages.messages import Success

class CertificateListAPI(ExceptionHandlerMixin, APIView):
    """
    List API for Certificates for a Profile
    """

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        title = serializers.CharField()
        description = serializers.CharField()
        organization = serializers.CharField()
        document = serializers.FileField()
        completion_date = serializers.DateField()
        is_published = serializers.BooleanField()

    def get(self, request, profile_id):
        certificates = get_list_certificate(profile=profile_id)
        serializer = self.OutputSerializer(certificates, many=True)
        return Response(serializer.data)

class CertificateDetailAPI(ExceptionHandlerMixin, APIView):
    """
    Detail API for Certificates for a Profile
    """
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        title = serializers.CharField()
        description = serializers.CharField()
        organization = serializers.CharField()
        document = serializers.FileField()
        completion_date = serializers.DateField()
        is_published = serializers.BooleanField()

    def get(self, request, pk, profile_id):
        certificate = get_detail_certificate(id=pk)

        serializer = self.OutputSerializer(certificate, many=False,)

        return Response(serializer.data)


class CertificateCreateAPI(ExceptionHandlerMixin, APIView):
    """
    Create Api for Certificates
    """
    permission_classes = [IsAuthenticatedAndProfileOwner, ]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        organization = serializers.CharField()
        document = serializers.FileField()
        completion_date = serializers.DateField()

    class OutputSerializer(InputSerializer):
        id = serializers.IntegerField()

    def post(self, request, profile_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_certificate = add_certificate(
            **serializer.validated_data,
            user=request.user,
            profile_id=profile_id)

        res = self.OutputSerializer(instance=new_certificate, many=False,).data
        return Response(data=res, status=status.HTTP_201_CREATED)

class CertificateUpdateAPI(ExceptionHandlerMixin, APIView):
    """
    Update API for Certificate
    """
    permission_classes = [IsAuthenticatedAndProfileOwner, ]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        organization = serializers.CharField()
        document = serializers.FileField()
        completion_date = serializers.DateField()

    class OutputSerializer(InputSerializer):
        id = serializers.IntegerField()

    def put(self, request, profile_id, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_certificate = update_certificate(
            id=pk,
            profile_id=profile_id,
            user=request.user,
            **serializer.validated_data)

        res = self.OutputSerializer(instance=updated_certificate, many=False,).data
        return Response(data=res, status=status.HTTP_200_OK)


class CertificateDeleteAPI(ExceptionHandlerMixin, APIView):
    """
    Delete Api for Certificate
    """

    def delete(self, request, profile_id, pk):
        delete_certificate(
            id=pk,
            user=request.user)

        return Response(
            {'message': Success.DELETED_SUCCESSFULLY},
            status=status.HTTP_200_OK)
