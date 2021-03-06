# Generated by Django 2.2 on 2020-12-11 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128, unique=True, verbose_name='项目编号')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='项目名称')),
                ('remark', models.TextField(max_length=256, verbose_name='备注')),
                ('create_time', models.DateField(verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
                'db_table': 'project',
                'ordering': ['-create_time'],
            },
        ),
    ]
