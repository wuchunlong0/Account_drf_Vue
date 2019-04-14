# Generated by Django 2.1 on 2019-04-14 09:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('taxNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(max_length=200)),
                ('bank', models.CharField(blank=True, max_length=200, null=True)),
                ('bankAccount', models.CharField(blank=True, max_length=200, null=True)),
                ('contact', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=200)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('type', models.CharField(choices=[('Design', 'Design'), ('Other', 'Other'), ('Manufacture', 'Manufacture')], default='Design', max_length=20)),
                ('content', models.CharField(default='', max_length=200)),
                ('sizeWidth', models.FloatField(blank=True, default=1, null=True)),
                ('sizeHeight', models.FloatField(blank=True, default=1, null=True)),
                ('priceMaterial', models.FloatField(blank=True, default=0, null=True)),
                ('price', models.FloatField(default=0)),
                ('quantity', models.FloatField(default=1)),
                ('priceTotal', models.FloatField(default=0)),
                ('taxPercent', models.FloatField(choices=[(0, 0), (6, 6), (17, 17)], default=0)),
                ('priceIncludeTax', models.FloatField(default=0)),
                ('checkout', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.Company')),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='account.Material')),
            ],
        ),
    ]
