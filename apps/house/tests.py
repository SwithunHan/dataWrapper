import os
import django
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataWrapper.settings')
django.setup()

if __name__ == '__main__':
    from house import models

    queryset = models.Houseinfo.objects.select_related("community").annotate(
        value=Count("housetype"))
    print(queryset.query)
