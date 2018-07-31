from django.contrib import admin
from .models import PaintEstimate

# Only allow business owners to see and update their own estimates
class PaintEstimateAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'bedroom_price', 'master_bedroom_price',
                    'bathroom_price', 'master_bathroom_price',
                    'living_room_price', 'stairway_cost', 'kitchen_price',
                    'ceiling_cost','ceiling_trim_cost',
                    'baseboard_trim_cost', 'other_price')

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(PaintEstimateAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and \
                    str(request.user) != str(obj.company_name):
            return False
        return True

    def queryset(self, request):
        if request.user.is_superuser:
            return PaintEstimate.objects.all()
        return PaintEstimate.objects.filter(company_name=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.company_name = request.user
        obj.save()

admin.site.register(PaintEstimate, PaintEstimateAdmin)

