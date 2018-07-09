# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from loginsys.views import login, logout, register, profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^login/$', login),
                  url(r'^logout/$', logout),
                  url(r'^register/$', register),
                  url(r'^profile/$', profile),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
