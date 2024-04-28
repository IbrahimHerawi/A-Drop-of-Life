from django.contrib import admin

from .models import (
    BloodGroup,
    Donor,
    Donation,
    Patient,
    Request,
)


admin.site.register(BloodGroup)
admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(Patient)
admin.site.register(Request)
