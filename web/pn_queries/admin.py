from django.contrib import admin
from .models import Oo, Owner, Service, Pn_query

admin.site.register(Oo)
admin.site.register(Owner)
admin.site.register(Service)

@admin.register(Pn_query)
class View_queries(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(active=True)
    list_display = ("date_create", "id_oo", "id_owner", "text", "date_end", "service", "comment")
    list_filter = ("date_create", "id_oo", "service")
