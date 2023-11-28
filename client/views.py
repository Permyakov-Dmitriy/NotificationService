from django.shortcuts import get_object_or_404

from rest_framework import views, permissions, status
from rest_framework.response import Response

from .models import ClientModel
from .serializer import ClientSerializer


class ClientApiView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.data["phone_number"]
            tag = serializer.data["tag"]
            timezone = serializer.data["timezone"]

            operator_code = phone_number[1:4]

            ClientModel.objects.create(
                phone_number=phone_number,
                operator_code=operator_code,
                tag=tag,
                timezone=timezone,
            )

    def put(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(ClientModel, pk)

        serializer = ClientSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = get_object_or_404(ClientModel, pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)