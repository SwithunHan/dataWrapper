from django.contrib import admin

# Register your models here.

from .models import Office, OfficeArea, OfficeType, Company, OfficeSkills


class OfficeAdmin(admin.ModelAdmin):
    list_display = ['officeType', 'company', 'get_skills', 'experience', 'salary']


class OfficeAreaAdmin(admin.ModelAdmin):
    list_display = ['name']


class OfficeTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['officeArea', 'name']


class OfficeSkillsAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Office, OfficeAdmin)
admin.site.register(OfficeArea, OfficeAreaAdmin)
admin.site.register(OfficeType, OfficeTypeAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(OfficeSkills, OfficeSkillsAdmin)
