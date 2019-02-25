from django.contrib import admin

from .models import *
class PackageAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


class EnrollmentAdmin(admin.ModelAdmin):
    search_fields = ['students__first', 'students__last', 'fao__first', 'fao__last', 'gc__first', 'gc__last', 'package__name',]
    filter_horizontal = ("students",)
    fields = ('package', ('packStart', 'packEnd'), 'students', 'fao', ('faoStart', 'faoEnd'), 'gc', ('gcStart', 'gcEnd'),)
    autocomplete_fields = ['package']    
    
admin.site.register(Counsoler)
admin.site.register(Student)
admin.site.register(Package, PackageAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
