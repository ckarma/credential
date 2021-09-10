from django.contrib import admin

# Register your models here.
from .models import Project, Server, Profile

# from . forms import ServerAdminForm

# class ServerAdmin(admin.ModelAdmin):
    # readonly_fields = ["key"]
#     form = ServerAdminForm

admin.site.register(Server)
admin.site.register(Project)
admin.site.register(Profile)