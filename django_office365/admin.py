from django.contrib import admin
from django_office365.models import UserOffice365ID

class AdminUserOffice365ID(admin.ModelAdmin):
    model = UserOffice365ID

admin.site.register(UserOffice365ID, AdminUserOffice365ID)
