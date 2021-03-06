# Generated by Django 4.0.4 on 2022-05-06 21:40

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sarlacc', '0004_rename_name_phenotype_id_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GWASSample',
            fields=[
                ('sample_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sarlacc.sample')),
                ('array', models.CharField(max_length=15)),
                ('PCs', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=8, max_digits=8), size=10)),
                ('barcode', models.CharField(max_length=10)),
            ],
            bases=('sarlacc.sample',),
        ),
    ]
