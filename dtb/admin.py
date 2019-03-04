from django.contrib import admin

# Register your models here.
from django.contrib import admin
from dtb.models import *
from django.apps import apps

for model in apps.get_app_config('dtb').models.values():
    admin.site.register(model)