# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='summary',
            field=ckeditor.fields.RichTextField(verbose_name=b'\xe6\xad\xa3\xe6\x96\x87'),
        ),
    ]
