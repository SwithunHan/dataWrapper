from django.contrib import admin

# Register your models here.
from house.models import Community, Houseinfo, Rentinfo

admin.site.register([Community, Houseinfo, Rentinfo])
