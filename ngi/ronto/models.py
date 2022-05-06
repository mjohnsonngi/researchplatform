from django.db import models
from django.contrib.postgres.fields import ArrayField
from sarlacc.models import Sample, Project, Run, RawData, ProcessedData

# Create your models here.


class WXSSample(Sample):
    barcode = models.CharField(max_length=10)
    series = models.CharField(max_length=15)

    @property
    def full_sample_id(self):
        "Returns the sample's full sample ID (FULLSMID)"
        return '%s^%s^%s' % (self.name.upper(), self.barcode.upper(), self.project)

    def __str__(self):
        return self.full_sample_id


class WXSProject(Project):
    center = models.CharField(max_length=10)
    WXS_CHOICES = [
                    ('G', "WGS"),
                    ('E', "WES"),
                    ('B', "WGS_WES"),
                    ('U', "Unknown"),
                ]
    wxs = models.CharField(
                    max_length=1, choices=WXS_CHOICES, default='U')

    def full_name(self):
        "Returns the project's full name"
        return '%s_%s_%s_%s' % (self.start_date.strftime("%y%m"), self.center.upper(), self.wxs, self.name.upper())

    def __str__(self):
        return self.full_name()


class WXSRun(Run):
    pipeline = models.CharField(max_length=8)
    gpu = models.BooleanField(default=False)
    REFERENCE_GENOME_CHOICES = [
                            ('h', "hg19"),
                            ('7', "GRCh37"),
                            ('8', "GRCh38"),
                            ('T', "T2T"),
                            ('U', "Unknown"),
                        ]
    reference_genome = models.CharField(
                        max_length=1, choices=REFERENCE_GENOME_CHOICES, default='U')
    align_version = models.CharField(max_length=20, blank=True)
    gatk_version = models.CharField(max_length=20, blank=True)
    samtools_version = models.CharField(
                        max_length=20, blank=True)
    RUN_TYPE_CHOICES = [
                            ('P', "Padded Exome"),
                            ('E', "Exome"),
                            ('G', "Genome"),
                        ]
    run_type = models.CharField(
                        max_length=1, choices=RUN_TYPE_CHOICES, default='P')
    bedtools_version = models.CharField(
                        max_length=20, blank=True)
    picard_version = models.CharField(
                        max_length=20, blank=True)

    def __str__(self):
        return '%s_%s_%s' % (self.sample, self.pipeline, self.date_added.isoformat())


class WXSRawData(RawData):
    TYPE_CHOICES = [
                    ('I', "interleaved fastq"),
                    ('C', "cram"),
                    ('B', "bam"),
                    ('P', "paired-end fastq"),
                ]
    type = models.CharField(
                        max_length=1, choices=TYPE_CHOICES)
    flowcell = models.CharField(max_length=10)
    lane = models.CharField(max_length=1)


class WXSProcessedData(ProcessedData):
    RGcrams = ArrayField(models.CharField(max_length=1, blank=True))
    ready_bam = models.CharField(max_length=1, blank=True)
    gvcf = models.CharField(max_length=1, blank=True)
    coverage = models.DecimalField(max_digits=5,
                                   decimal_places=2, blank=True)
    freemix = models.DecimalField(max_digits=6,
                                  decimal_places=5, blank=True)
    titv = models.DecimalField(max_digits=3, decimal_places=2, blank=True)
