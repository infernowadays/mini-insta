from django.conf.urls import url
from post.views import posts, post, like, comment, profile, new_post, avatar, user_profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^(?P<user_name>[a-zA-z0-9]+)/profile/$', user_profile),

                  url(r'^profile/avatar/$', avatar),
                  url(r'^post/new/$', new_post),
                  url(r'^profile/me/$', profile),
                  url(r'^post/like/(?P<post_id>\d+)/$', like),
                  url(r'^post/comment/(?P<post_id>\d+)/$', comment),
                  url(r'^post/(?P<post_id>\d+)/$', post),
                  url(r'^$', posts),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
