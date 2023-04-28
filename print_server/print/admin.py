from django.contrib import admin
from print.models import PrintModel


# Register your models here.
class PrintAdmin(admin.ModelAdmin):
    list_display_links = ['id', 'team_name', 'team_id']
    list_display = ['id', 'team_name', 'team_id', 'submit_time', 'status']
    list_filter = ['status']


admin.site.register(PrintModel, PrintAdmin)
