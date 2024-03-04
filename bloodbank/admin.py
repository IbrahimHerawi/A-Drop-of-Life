from django.contrib import admin

from .models import (
    BloodGroup,
    Donation,
    Request,
)


admin.site.register(BloodGroup)
admin.site.register(Donation)
admin.site.register(Request)
