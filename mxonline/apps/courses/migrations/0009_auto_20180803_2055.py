# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-03 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='课程老师提示须知'),
        ),
        migrations.AddField(
            model_name='course',
            name='youneed_know',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='课程须知'),
        ),
    ]
