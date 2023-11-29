from django.contrib import admin

from .models import ClientModel, TagModel, LinkTagAndClientModel


admin.site.register(ClientModel)
admin.site.register(TagModel)
admin.site.register(LinkTagAndClientModel)
