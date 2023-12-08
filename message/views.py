from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import views, status
from rest_framework.response import Response

from mailing.models import MailingModel

from .models import MessageModel
from .serializer import MessageSerializer


class StatisticsMessagesApiView(views.APIView):
    def get(self, request, *args, **kwargs):
        mailing_id = request.GET.get("id")

        mailing_instance = get_object_or_404(klass=MailingModel, pk=mailing_id)

        result = MessageModel.objects.filter(
            Q(mailing_id=mailing_instance) & Q(status="Delivered")
        )

        serializer = MessageSerializer(data=result, many=True)

        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)
