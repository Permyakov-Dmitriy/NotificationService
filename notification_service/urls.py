from django.contrib import admin
from django.urls import path, include

from mailing.views import MailingApiView
from client.views import ClientApiView
from message.views import StatisticsMessagesApiView


url_api_patterns = [
    path("mailing", MailingApiView.as_view(), name='mailing'),
    path("client", ClientApiView.as_view(), name='client'),
    path("statistics_messages/<int:pk>", StatisticsMessagesApiView.as_view()), 
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(url_api_patterns)),
]
