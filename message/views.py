from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import views, status
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from mailing.models import MailingModel

from .models import MessageModel
from .serializer import MessageSerializer


class StatisticsMessagesApiView(views.APIView):
    @extend_schema(
        request=MessageSerializer,
            parameters=[
                OpenApiParameter(
                    name='id',
                    type=int,
                    location=OpenApiParameter.PATH,
                    description='Description of the query parameter',
                    required=True,
                ),
            ],
        responses={
            200: OpenApiResponse(
                response=MessageSerializer(many=True),
            ),
            404: OpenApiResponse(
                response=inline_serializer(
                    name="Error", fields={}
                ),
            )
        }
    )

    def get(self, request, *args, **kwargs):
        mailing_id = request.GET.get("id")

        mailing_instance = get_object_or_404(klass=MailingModel, pk=mailing_id)

        result = MessageModel.objects.filter(
            Q(mailing_id=mailing_instance) & Q(status="Delivered")
        )

        serializer = MessageSerializer(data=result, many=True)

        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)
