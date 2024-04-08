from django.core.cache import cache
from service.models import Collect


def get_collects_cache():
    """Caching the collect-queryset on 300 seconds"""
    collects_cache = cache.get('collects')
    if collects_cache:
        return collects_cache
    else:
        queryset = Collect.objects.all()
        cache.set('collects', queryset, 300)
    return queryset
