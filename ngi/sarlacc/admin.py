from django.contrib import admin

# Register your models here.
from .models import Participant, Phenotype, Project, Sample

admin.site.register(Participant)
admin.site.register(Phenotype)
admin.site.register(Project)
admin.site.register(Sample)
