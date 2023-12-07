from django.contrib import admin
from django.urls import path, include

from mailing.views import MailingApiView, TestCeleryView
from client.views import ClientApiView
from message.views import StatisticsMessagesApiView


url_api_patterns = [
    path("mailing", MailingApiView.as_view()),
    path("client", ClientApiView.as_view()),
    path("statistics_messages/<int:pk>", StatisticsMessagesApiView.as_view()), 
    path("test", TestCeleryView.as_view())
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(url_api_patterns)),
]
