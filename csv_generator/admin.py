from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    SchemaColumn,
    DataSchema,
    GeneratedCSV,
)


class SchemaColumnInLine(admin.TabularInline):
    model = SchemaColumn
    extra = 1


@admin.register(DataSchema)
class DataSchemaAdmin(admin.ModelAdmin):
    inlines = [SchemaColumnInLine]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(SchemaColumn)
admin.site.register(GeneratedCSV)
