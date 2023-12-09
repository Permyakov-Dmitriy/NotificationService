from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import views, status, serializers
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from .models import ClientModel
from .serializer import ClientSerializer
from .utils.link_tags import create_link_tags


class ClientApiView(views.APIView):
    @extend_schema(
        request=ClientSerializer,
        responses={
            201: OpenApiResponse(),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="Error input data",
                    fields={"detail": serializers.CharField()},
                )
            )
        }
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.data["phone_number"]
            tags = serializer.data.get('tags', None)
            timezone = serializer.data["timezone"]

            operator_code = phone_number[1:4]

            client_instance = ClientModel.objects.create(
                phone_number=phone_number,
                operator_code=operator_code,
                timezone=timezone,
            )

            if tags is not None:
                create_link_tags(client_instance, tags)

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=ClientSerializer,
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
            200: ClientSerializer(),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="Error input data",
                    fields={"detail": serializers.CharField()},
                )
            ),
            404: OpenApiResponse(
                response=inline_serializer(
                    name="Not Found",
                    fields={"detail": serializers.CharField()},
                )
            )
        }
    )
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        client_id = request.GET.get("id")
        instance = get_object_or_404(klass=ClientModel, pk=client_id)

        serializer = ClientSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=ClientSerializer,
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
            204: OpenApiResponse(),
            404: OpenApiResponse(
                response=inline_serializer(
                    name="Not Found",
                    fields={"detail": serializers.CharField()},
                )
            )
        }
    )
    def delete(self, request, format=None):
        client_id = request.GET.get("id")

        instance = get_object_or_404(klass=ClientModel, pk=client_id)
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)