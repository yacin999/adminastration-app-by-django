# Generated by Django 2.2.6 on 2020-09-12 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_delete_loggedinuser'),
        ('dashboard', '0019_auto_20200909_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='canvastimetable',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='emploitemps',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering_date', models.DateTimeField(auto_now_add=True)),
                ('returned', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Staff')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='dashboard.Material')),
            ],
        ),
    ]
