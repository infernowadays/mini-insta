from django.conf.urls import url
from loginsys.views import login, register, LogoutRedirectView, LoginRedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^login/$', LoginRedirectView.as_view(), name='login'),
                  url(r'^logout/$', LogoutRedirectView.as_view(), name='logout'),
                  url(r'^register/$', register, name='register')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
