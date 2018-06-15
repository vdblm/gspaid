# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-15 10:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestTypeBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('wage_rule', models.CharField(default='0 0', max_length=128)),
            ],
        ),
        migrations.RenameField(
            model_name='requesttype',
            old_name='extra_information',
            new_name='information',
        ),
        migrations.RemoveField(
            model_name='requesttype',
            name='description',
        ),
        migrations.RemoveField(
            model_name='requesttype',
            name='name',
        ),
        migrations.CreateModel(
            name='ExchangeRequest',
            fields=[
                ('requesttypebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='workflow.RequestTypeBase')),
            ],
            options={
                'abstract': False,
            },
            bases=('workflow.requesttypebase', models.Model),
        ),
    ]
