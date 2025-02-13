from django.contrib import admin

from evoting.webapp.forms import Voter

# Register your models here.

from .models import *
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(Voter)

