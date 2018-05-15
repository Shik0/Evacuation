from django.contrib import admin
from .models import StuffAll, Country, Guest, StuffInside

# Register your models here.

#admin.site.register(StuffAll)
#admin.site.register(Country)

@admin.register(StuffAll)
class StuffAllAdmin(admin.ModelAdmin):
    list_display = ('name', 'department','position','start_date')
    list_filter = ('department',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

@admin.register(StuffInside)
class StuffAllAdmin(admin.ModelAdmin):
        list_display = ('name', 'department','position','start_date')
        list_filter = ('department',)

@admin.register(Guest)
class StuffAllAdmin(admin.ModelAdmin):
        list_display = ('name', 'guest_company','entry_date')
        list_filter = ('guest_company',)
