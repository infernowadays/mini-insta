from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from social import views as core_views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^', include('post.urls')),

    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^$', core_views.home, name='home'),
    url(r'^q/login/$', auth_views.login),
    url(r'^q/logout/$', auth_views.logout),
    url(r'^q/signup/$', core_views.signup),
    url(r'^q/settings/$', core_views.settings),
    url(r'^q/settings/password/$', core_views.password),

]
