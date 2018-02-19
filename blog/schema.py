import graphene

from graphene_django.types import DjangoObjectType

from . import models


class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post


class Query(graphene.ObjectType):
    tags = graphene.List(TagType)
    posts = graphene.List(PostType)

    def resolve_tags(self, info, **kwargs):
        return models.Tag.objects.all()

    def resolve_posts(self, info, **kwargs):
        return models.Post.objects.all()


schema = graphene.Schema(query=Query)
