from django.contrib import admin
from django.urls import path, include

from mailing.views import MailingApiView
from client.views import ClientApiView


url_api_patterns = [
    path("mailing/", MailingApiView.as_view()),
    path("client/", ClientApiView.as_view()),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(url_api_patterns)),
]
