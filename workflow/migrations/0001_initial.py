# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-21 18:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('financial', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('created', 'Created'), ('in_progress', 'In progress'), ('failed', 'Failed'), ('succeeded', 'Succeeded'), ('suspicious', 'Suspicious')], default='created', max_length=32)),
                ('attachment', models.FileField(upload_to='')),
                ('user_description', models.TextField()),
                ('employee_description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequestTypeBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('wage_rule', models.CharField(default='0 0', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRequestType',
            fields=[
                ('requesttypebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='workflow.RequestTypeBase')),
            ],
            options={
                'abstract': False,
            },
            bases=('workflow.requesttypebase', models.Model),
        ),
        migrations.CreateModel(
            name='RequestType',
            fields=[
                ('requesttypebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='workflow.RequestTypeBase')),
                ('amount', models.DecimalField(decimal_places=64, max_digits=128)),
                ('information', models.TextField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial.Currency')),
            ],
            bases=('workflow.requesttypebase',),
        ),
        migrations.AddField(
            model_name='request',
            name='request_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.RequestType'),
        ),
    ]
