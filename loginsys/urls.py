from django.conf.urls import url
from loginsys.views import LoginView, LogoutView, SignUpView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^login/$', LoginView.as_view(), name='login'),
                  url(r'^logout/$', LogoutView.as_view(), name='logout'),
                  url(r'^register/$', SignUpView.as_view(), name='register')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
