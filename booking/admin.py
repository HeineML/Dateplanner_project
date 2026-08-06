from django.contrib import admin
from .models import Unavailability, DateRequest


@admin.register(Unavailability)
class UnavailabilityAdmin(admin.ModelAdmin):
    list_display = ('date', 'note')


@admin.register(DateRequest)
class DateRequestAdmin(admin.ModelAdmin):
    list_display = ('date', 'activity', 'status', 'requested_by', 'created_at')
    list_filter = ('status',)
