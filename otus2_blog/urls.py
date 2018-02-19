from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from graphene_django.views import GraphQLView

from blog.schema import schema


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('', include('blog.urls')),
]
