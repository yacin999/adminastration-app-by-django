# Generated by Django 2.2.6 on 2020-10-16 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20201014_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='semestre',
            field=models.CharField(choices=[('1', 'S1'), ('2', 'S2'), ('3', 'S3'), ('4', 'S4'), ('5', 'S5'), ('6', 'S6'), ('7', 'M1'), ('8', 'M2'), ('9', 'M3'), ('10', 'M4')], max_length=10),
        ),
    ]