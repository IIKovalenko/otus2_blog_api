from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'posts', views.PostViewSet)


urlpatterns = [
    url(r'^posts/$', views.PostListView.as_view(), name='posts_list'),
    url(r'^posts/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^api/', include(router.urls)),
]
