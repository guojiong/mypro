# Generated by Django 2.2.6 on 2020-12-31 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0002_auto_20201221_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtype', models.CharField(max_length=128, verbose_name='材料分类')),
                ('mclass', models.CharField(max_length=128, verbose_name='材料小类')),
                ('mname', models.CharField(max_length=128, verbose_name='材料名称')),
                ('specifi', models.CharField(max_length=128, verbose_name='品牌/规格/型号')),
                ('num', models.IntegerField(verbose_name='数量')),
                ('unit', models.CharField(max_length=128, verbose_name='单位')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '库存',
                'verbose_name_plural': '库存',
                'db_table': 'store',
                'ordering': ['-mname'],
            },
        ),
        migrations.CreateModel(
            name='OutStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='出库日期')),
                ('outNo', models.CharField(max_length=128, unique=True, verbose_name='出库单号')),
                ('toWhere', models.CharField(max_length=128, verbose_name='出库去向')),
                ('num', models.IntegerField(verbose_name='数量')),
                ('receiver', models.CharField(max_length=128, verbose_name='领用人')),
                ('remark', models.TextField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store', verbose_name='库存id')),
            ],
            options={
                'verbose_name': '出库单',
                'verbose_name_plural': '出库单',
                'db_table': 'outstore',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='InStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='入库日期')),
                ('receiptNo', models.CharField(max_length=128, unique=True, verbose_name='入库单号')),
                ('mtype', models.CharField(max_length=128, verbose_name='材料分类')),
                ('mclass', models.CharField(max_length=128, verbose_name='材料小类')),
                ('mname', models.CharField(max_length=128, verbose_name='材料名称')),
                ('specifi', models.CharField(max_length=128, verbose_name='品牌/规格/型号')),
                ('num', models.IntegerField(verbose_name='数量')),
                ('unit', models.CharField(max_length=128, verbose_name='单位')),
                ('rate', models.CharField(blank=True, max_length=128, null=True, verbose_name='税率')),
                ('factory', models.CharField(blank=True, max_length=128, null=True, verbose_name='厂家名称')),
                ('materialfee', models.CharField(max_length=128, verbose_name='材料费')),
                ('price', models.CharField(max_length=128, verbose_name='单价')),
                ('buyer', models.CharField(max_length=128, verbose_name='采购员')),
                ('inspector', models.CharField(max_length=128, verbose_name='验收员')),
                ('storeloc', models.CharField(blank=True, max_length=128, null=True, verbose_name='仓库')),
                ('provider', models.CharField(max_length=128, verbose_name='供应商')),
                ('remark', models.TextField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '入库单',
                'verbose_name_plural': '入库单',
                'db_table': 'instore',
                'ordering': ['-date'],
            },
        ),
    ]