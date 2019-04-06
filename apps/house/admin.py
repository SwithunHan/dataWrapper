from django.contrib import admin

# Register your models here.
from house.models import Community, Houseinfo, Rentinfo, Sellinfo

admin.site.register([Community, Houseinfo, Rentinfo, Sellinfo])
