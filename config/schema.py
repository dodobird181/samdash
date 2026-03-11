"""Root GraphQL schema combining all app schemas."""

import graphene
import dashboard.schema
import rss.schema


class Query(dashboard.schema.Query, rss.schema.Query, graphene.ObjectType):
    """Root query combining all app queries."""

    pass


schema = graphene.Schema(query=Query)
