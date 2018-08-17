# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-16 13:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0002_auto_20180615_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_amount', models.DecimalField(decimal_places=64, max_digits=128)),
                ('to_amount', models.DecimalField(decimal_places=64, max_digits=128)),
                ('status', models.CharField(choices=[('created', 'Created'), ('failed', 'Failed'), ('succeeded', 'Succeeded')], default='created', max_length=32)),
                ('from_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='going_transaction_set', to='financial.Currency')),
                ('to_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coming_transaction_set', to='financial.Currency')),
            ],
        ),
    ]
