# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-01-10 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uphone', models.CharField(max_length=20, verbose_name='电话号码')),
                ('upwd', models.CharField(max_length=20, verbose_name='密码')),
                ('uemail', models.EmailField(max_length=254, verbose_name='电子邮件')),
                ('uname', models.CharField(max_length=20, verbose_name='用户名')),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
    ]
