from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView

from mailing.views import MailingApiView
from client.views import ClientApiView
from message.views import StatisticsMessagesApiView


url_api_patterns = [
    path("schema", SpectacularAPIView.as_view(), name="schema"),
    path("docs", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("mailing", MailingApiView.as_view(), name='mailing'),
    path("client", ClientApiView.as_view(), name='client'),
    path("statistics_messages", StatisticsMessagesApiView.as_view(), name='statistics'), 
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(url_api_patterns)),
]
