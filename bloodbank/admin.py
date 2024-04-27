from django.contrib import admin

from .models import (
    BloodGroup,
    Donor,
    Donation,
    Request,
)


admin.site.register(BloodGroup)
admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(Request)
