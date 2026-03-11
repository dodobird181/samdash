"""RSS API views."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rss.models import RSSEntry
from rss.api.serializers import RSSEntrySerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def entry_list(request):
    """Return latest RSS entries, optional ?limit=N query param."""
    limit = request.query_params.get("limit")
    entries = RSSEntry.objects.select_related("feed").order_by("-published_at")
    if limit is not None:
        try:
            entries = entries[: int(limit)]
        except (ValueError, TypeError):
            pass
    serializer = RSSEntrySerializer(entries, many=True)
    return Response(serializer.data)
