from django.contrib import admin

# Register your models here.
from pcod_finder.models import Usertable,PCOSPrediction,Expert_details  # Import your model here

admin.site.register(Usertable)
admin.site.register(PCOSPrediction)
admin.site.register(Expert_details)



