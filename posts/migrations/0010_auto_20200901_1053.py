# Generated by Django 2.2.9 on 2020-09-01 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_merge_20200803_1721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',)},
        ),
    ]