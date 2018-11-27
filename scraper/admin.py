from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ProductData

# Register your models here.

@admin.register(ProductData)
class ViewAdmin(ImportExportModelAdmin):
    pass
