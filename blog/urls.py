from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'posts', views.PostViewSet)


urlpatterns = [
    url(r'^', include(router.urls))
]
