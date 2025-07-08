from django.contrib import admin
from django.http import HttpResponse
from .models import OrganizationModel, AssortmentModel, ManagerModel, OrderModel, OrderAssortmentTableModel

admin.site.register(AssortmentModel)
admin.site.register(OrganizationModel)

class ManagerModelAdmin(admin.ModelAdmin):
  list_display = ("name", "organization", "user")
  list_filter = ('organization__name','name', 'user')
admin.site.register(ManagerModel, ManagerModelAdmin)

class OrderAssortmentlInline(admin.TabularInline):
    model = OrderAssortmentTableModel
    extra = 1

class OrderModelAdmin(admin.ModelAdmin):
  list_display = ("number", "date","organization","summa")
  list_filter = ('date', 'number','organization')
  search_fields = ('number', 'date', 'organization__name') 
  ordering = ('date',)
  inlines = [OrderAssortmentlInline]

admin.site.register(OrderModel, OrderModelAdmin)

def make_count(modeladmin, request, queryset):
    #queryset.update(price='summa/count')
    return HttpResponse("Selected lines were successfully update.")
make_count.short_description = "Count field count"

# class OrderAssortmentTableModelAdmin(admin.ModelAdmin):
#    ordering = ('num',)
#    actions = [make_count]
#    readonly_fields = ('num','assortiment','summa')

# admin.site.register(OrderAssortmentTableModel, OrderAssortmentTableModelAdmin)