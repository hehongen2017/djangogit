# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-03 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20180803_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='', max_length=300, verbose_name='课程老师提示须知'),
        ),
        migrations.AlterField(
            model_name='course',
            name='youneed_know',
            field=models.CharField(default='', max_length=300, verbose_name='课程须知'),
        ),
    ]
