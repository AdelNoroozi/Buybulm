from django.contrib import admin

from accounts.models import *

admin.site.register(BaseUser)
admin.site.register(Profile)
admin.site.register(Admin)
