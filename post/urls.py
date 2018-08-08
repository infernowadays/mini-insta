from django.conf.urls import url
from post.views import (
    NewPostView,
    PostListView,
    CommentView,
    PostDetailView,
    ProfilePage,
    UserProfilePage,
    ChangeAvatarView,
    LikeView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^(?P<user_name>[a-zA-z0-9.]+)/profile/$', UserProfilePage.as_view(), name='user_profile'),
                  url(r'^profile/avatar/$', ChangeAvatarView.as_view(), name='change_avatar'),
                  url(r'^post/new/$', NewPostView.as_view(), name='new_post'),
                  url(r'^profile/me/$', ProfilePage.as_view(), name='profile'),
                  url(r'^post/like/(?P<post_id>\d+)/$', LikeView.as_view(), name='like'),
                  url(r'^post/comment/(?P<post_id>\d+)/$', CommentView.as_view(), name='comment'),
                  url(r'^post/(?P<post_id>\d+)/$', PostDetailView.as_view(), name='post'),
                  url(r'^$', PostListView.as_view(), name='posts'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
