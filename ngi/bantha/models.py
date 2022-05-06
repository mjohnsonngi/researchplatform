from django.db import models
from django.contrib.postgres.fields import ArrayField
from sarlacc.models import Sample, Project, Run, RawData, ProcessedData

# Create your models here.


class GWASSample(Sample):
    array = models.CharField(max_length=15)
    PCs = ArrayField(models.DecimalField(
        max_digits=8, decimal_places=8), size=10)
    barcode = models.CharField(max_length=10)

    def iid(self):
        "Returns the sample's IID"
        return '%s^%s^%s_%s' % (self.participant.name, self.barcode, self.participant.cohort, self.array)

    def __str__(self):
        return self.iid()
