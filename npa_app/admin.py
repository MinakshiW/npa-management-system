from django.contrib import admin
from .models import NPA, NPAStatusHistory

admin.site.register(NPA)
admin.site.register(NPAStatusHistory)
