from django.contrib import admin
from .models import MasterData, Slot, Booking

admin.site.register(MasterData)
admin.site.register(Slot)
admin.site.register(Booking)
