from django.conf.urls import url
from loginsys.views import login, logout, register, profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^login/$', login, name='login'),
                  url(r'^logout/$', logout, name='logout'),
                  url(r'^register/$', register, name='register'),
                  url(r'^profile/$', profile, name='profile'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
