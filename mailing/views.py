from django.shortcuts import get_object_or_404

from rest_framework import views, permissions, status
from rest_framework.response import Response

from message.models import MessageModel

from .models import MailingModel
from .serializer import MailingSerializer


class MailingApiView(views.APIView):
    def get(self, request, *args, **kwargs):
        serializer = MailingSerializer(data=MailingModel.objects.all(), many=True)

        serializer.is_valid()

        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = MailingSerializer(data=request.data)

        if serializer.is_valid():
            launch_time = serializer.data["launch_time"]
            finish_time = serializer.data["finish_time"]
            message_text = serializer.data["message_text"]
            filter_tags = serializer.data["filter_tags"]
            filter_operator = serializer.data["filter_operator"]

            MailingModel.objects.create(
                launch_time=launch_time,
                finish_time=finish_time,
                message_text=message_text,
                filter_tags=filter_tags,
                filter_operator=filter_operator
            )

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(ClientModel, pk)

        serializer = MailingSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        instance = get_object_or_404(MailingModel, pk)

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)