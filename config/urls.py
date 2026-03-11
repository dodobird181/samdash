"""Root URL configuration for samdash."""

from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("api/", include("dashboard.api.urls")),
    path("api/rss/", include("rss.api.urls")),
    path("", include("dashboard.urls")),
]
