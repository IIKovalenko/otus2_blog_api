from rest_framework import viewsets
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from . import models
from . import serializers


class TagViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.select_related('user').prefetch_related('tags')


class PostListView(ListView):
    model = models.Post
