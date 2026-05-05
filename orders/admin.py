from django.contrib import admin
from .models import WorkOrder


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display  = ['code', 'title', 'status', 'priority', 'assigned_to', 'due_date']
    list_filter   = ['status', 'priority']
    search_fields = ['code', 'title']
    readonly_fields = ['code', 'created_at', 'updated_at']
