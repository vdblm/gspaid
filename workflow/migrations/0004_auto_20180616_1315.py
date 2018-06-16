# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-16 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_auto_20180616_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('in_progress', 'In progress'), ('failed', 'Failed'), ('succeeded', 'Succeeded'), ('suspicious', 'Suspicious')], default='created', max_length=32),
        ),
    ]