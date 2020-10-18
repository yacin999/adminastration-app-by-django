# Generated by Django 2.2.6 on 2020-10-14 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20201009_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salle',
            name='type_of',
            field=models.CharField(choices=[('1', 'TP'), ('2', 'TD'), ('3', 'Cours')], max_length=10),
        ),
        migrations.AlterField(
            model_name='science',
            name='nature',
            field=models.CharField(choices=[('1', 'TP'), ('2', 'TD'), ('3', 'Cours')], max_length=20),
        ),
    ]