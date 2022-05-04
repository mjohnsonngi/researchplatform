from django.contrib.postgres.fields import ArrayField
from django.db import models


class Participant(models.Model):
    pheno_id = models.CharField(max_length=20, unique=True)
    date_added = models.DateField(auto_now_add=True)
    other_ids = models.ForeignKey(
        'self',
        on_delete=models.DO_NOTHING,
        related_name="alias",
        related_query_name="aliases",
        blank=True
    )

    def __str__(self):
        return self.pheno_id.upper()


class Phenotype(models.Model):
    name = models.CharField(max_length=15)
    date_added = models.DateField(auto_now_add=True)
    date_effective = models.DateField()
    cohort = models.CharField(max_length=10)
    date_of_birth = models.DateField(blank=True)
    participant = models.ForeignKey(
        'Participant',
        on_delete=models.DO_NOTHING,
        related_name="phenotype",
        related_query_name="phenotypes",
    )
    RACE_CHOICES = [
        ('W', "White"),
        ('B', "Black/African American"),
        ('A', "Asian"),
        ('N', "American Indian/Native American"),
        ('M', "More than one race"),
        ('P', "Native Hawaiian or Other Pacific Islander"),
        ('U', "Unknown"),
    ]
    race = models.CharField(max_length=1, choices=RACE_CHOICES, default='U')
    ETHNICITY_CHOICES = [
        ('H', "Hispanic or Latinx"),
        ('N', "Not Hispanic or Latinx"),
        ('U', "Unknown"),
    ]
    ethnicity = models.CharField(
        max_length=1, choices=ETHNICITY_CHOICES, default='U')
    APOE_CHOICES = [
        ('22', "22"),
        ('23', "23"),
        ('24', "24"),
        ('33', "33"),
        ('34', "34"),
        ('44', "44"),
        ('NA', "NA"),
        ('UK', "Unknown"),
    ]
    apoe = models.CharField(max_length=2, choices=APOE_CHOICES, default='UK')
    education = models.PositiveSmallIntegerField()
    FINAL_CC_STATUS_CHOICES = [
        ('AD', (
                ('AD', 'AD'),
                ('AAN', 'ADAD_Affected_Non_carrier'),
                ('AAC', 'ADAD_Affected_carrier'),
                ('ANC', 'ADAD_Non_carrier'),
                ('APC', 'ADAD_Presymptomatic_carrier'),
                ('NAD', 'Neuro_AD'),
                ('NAD', 'Neuro_AD_DLB'),
                ('NAF', 'Neuro_AD_FTD'),
                ('NAP', 'Neuro_AD_PD'),
                ('NPA', 'Neuro_PreSymptomatic_AD'),
                ('DEM', 'Dementia'),
            )
         ),
        ('Control', (
                ('AUN', 'ADAD_Unaffected_Non_carrier'),
                ('CO', 'CO'),
                ('MUN', 'MAPT_Unaffected_Non_carrier'),
                ('NCO', 'Neuro_CO'),
                ('OCO', 'OT(CO)'),
                ('PUN', 'PGRN_Unaffected_Non_carrier'),
            )
         ),
        ('Other', (
                ('C9+', 'C9ORF72+'),
                ('MAN', 'MAPT_Affected_Non_carrier'),
                ('MAC', 'MAPT_Affected_carrier'),
                ('MNC', 'MAPT_Non_carrier'),
                ('MPC', 'MAPT_Presymptomatic_carrier'),
                ('MC', 'MAPT_carrier'),
                ('PAN', 'PGRN_Affected_Non_carrier'),
                ('PAC', 'PGRN_Affected_carrier'),
                ('PNC', 'PGRN_Non_carrier'),
                ('PPC', 'PGRN_Presymptomatic_carrier'),
                ('PC', 'PGRN_carrier'),
                ('NAL', 'Neuro_ALS'),
                ('NDL', 'Neuro_DLB'),
                ('NFT', 'Neuro_FTD'),
                ('NOT', 'Neuro_OT'),
                ('NPD', 'Neuro_PD'),
                ('NPS', 'Neuro_PSP'),
                ('PRY', 'Neuro_Parry'),
                ('OT', 'OT'),
                ('DLB', 'DLB'),
                ('FTD', 'FTD'),
                ('PD', 'PD'),
            )
         ),
        ('CHECK', (
                ('N19', 'CC_npthprim19'),
                ('L2P', 'LRRK2_positive'),
            )
         ),
        ('NO', (
                ('NOS', 'NO-SHARING'),
                ('OSC', 'OSC'),
                ('UNK', 'Unknown'),
            )
         ),
    ]
    final_cc_status = models.CharField(
        max_length=3, choices=FINAL_CC_STATUS_CHOICES, default='UNK')
    CDR_CHOICES = [
        ('A', "0"),
        ('B', "0.5"),
        ('C', "1"),
        ('D', "2"),
        ('E', "3"),
        ('U', "Unknown"),
    ]
    cdr_final = models.CharField(
        max_length=1, choices=CDR_CHOICES, default='U')
    cdr_expiration = models.CharField(
        max_length=1, choices=CDR_CHOICES, default='U')
    age_onset = models.PositiveSmallIntegerField(blank=True)
    age_at_last = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        return '%s_%s' % (self.project.pheno_id.upper(), self.date_effective.isoformat())


class Sample(models.Model):
    name = models.CharField(max_length=20)
    date_collected = models.DateField(blank=True)
    date_added = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        'Project',
        on_delete=models.DO_NOTHING,
        related_name="samples",
        related_query_name="sample",
    )
    participant = models.ForeignKey(
        'Participant',
        on_delete=models.DO_NOTHING,
        related_name="samples",
        related_query_name="sample",
    )

    def __str__(self):
        return '%s_%s' % (self.name.upper(), self.project)


class WXSSample(Sample):
    barcode = models.CharField(max_length=10)
    series = models.CharField(max_length=15)

    @property
    def full_sample_id(self):
        "Returns the sample's full sample ID (FULLSMID)"
        return '%s^%s^%s' % (self.name.upper(), self.barcode.upper(), self.project)

    def __str__(self):
        return self.full_sample_id


class Project(models.Model):
    name = models.CharField(max_length=30)
    date_added = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    last_modified = models.DateField(auto_now=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name.upper()

    def full_name(self):
        "Returns the project's full name"
        return '%s_%s' % (self.start_date.strftime("%y%m"), self.name.upper())


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


class Run(models.Model):
    date_added = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    basename = models.CharField(max_length=30)
    directory = models.CharField(max_length=255)

    def __str__(self):
        return '%s_%s' % (self.sample, self.date_added.isoformat())


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
    samtools_version = models.CharField(max_length=20, blank=True)
    RUN_TYPE_CHOICES = [
            ('P', "Padded Exome"),
            ('E', "Exome"),
            ('G', "Genome"),
        ]
    run_type = models.CharField(
        max_length=1, choices=RUN_TYPE_CHOICES, default='P')
    bedtools_version = models.CharField(max_length=20, blank=True)
    picard_version = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return '%s_%s_%s' % (self.sample, self.pipeline, self.date_added.isoformat())


class RawData(models.Model):
    archived = models.BooleanField(default=False)
    sample = models.ForeignKey(
        'Sample',
        on_delete=models.DO_NOTHING,
        related_name="raw_data",
    )
    date_added = models.DateField(auto_now_add=True)
    file_basename = models.CharField(max_length=30, blank=True)
    directory = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.sample


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


class ProcessedData(models.Model):
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(blank=True)
    sample = models.ForeignKey(
        'Sample',
        on_delete=models.DO_NOTHING,
        related_name="processed_data",
    )
    run = models.ForeignKey(
        'Run',
        on_delete=models.DO_NOTHING,
        related_name="processed_data",
    )


class WXSProcessedData(ProcessedData):
    RGcrams = ArrayField(models.CharField(max_length=1, blank=True))
    ready_bam = models.CharField(max_length=1, blank=True)
    gvcf = models.CharField(max_length=1, blank=True)
    coverage = models.DecimalField(..., max_digits=5,
                                   decimal_places=2, blank=True)
    freemix = models.DecimalField(..., max_digits=6,
                                  decimal_places=5, blank=True)
    titv = models.DecimalField(..., max_digits=3, decimal_places=2, blank=True)
