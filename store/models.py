from django.db import models
from project.models import Project


# Create your models here.
class Store(models.Model):
    
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, verbose_name='所属项目')
    mtype = models.CharField(max_length=128, verbose_name='材料分类')
    mclass = models.CharField(max_length=128, verbose_name='材料小类')
    mname = models.CharField(max_length=128, verbose_name='材料名称')
    specifi = models.CharField(max_length=128, verbose_name='品牌/规格/型号')
    num = models.IntegerField(verbose_name='数量')
    price = models.CharField(max_length=10, verbose_name='税后单价')
    unit = models.CharField(max_length=128, verbose_name='单位')
    
    def __str__(self):
        return '[%s]' % (self.mname)
    
    class Meta:
        ordering = ['-mname']
        db_table = 'store'
        verbose_name = '库存'
        verbose_name_plural = '库存'


class InStore(models.Model):
    
    date = models.DateField(verbose_name='入库日期')
    receiptNo = models.CharField(max_length=128, unique=True, verbose_name='入库单号')
    mtype = models.CharField(max_length=128, verbose_name='材料分类')
    mclass = models.CharField(max_length=128, verbose_name='材料小类')
    mname = models.CharField(max_length=128, verbose_name='材料名称')
    specifi = models.CharField(max_length=128, verbose_name='品牌/规格/型号')
    num = models.IntegerField(verbose_name='数量')
    unit = models.CharField(max_length=128, verbose_name='单位')
    rate = models.CharField(max_length=128, verbose_name='税率', null=True, blank=True)
    factory = models.CharField(max_length=128, verbose_name='厂家名称', null=True, blank=True)
    materialfee = models.CharField(max_length=128, verbose_name='材料费')
    price = models.CharField(max_length=10, verbose_name='税后单价')
    buyer = models.CharField(max_length=128, verbose_name='采购员')
    inspector = models.CharField(max_length=128, verbose_name='验收员')
    storeloc = models.CharField(max_length=128, verbose_name='仓库', null=True, blank=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, verbose_name='所属项目')
    provider = models.CharField(max_length=128, verbose_name='供应商')
    remark = models.TextField(max_length=256, verbose_name='备注', null=True, blank=True)
    
    def __str__(self):
        return '[%s]_%s_%s_%s_%s_%s' % (self.mname, self.mtype, self.mclass, self.specifi, self.project, self.factory)
    
    class Meta:
        ordering = ['-date']
        db_table = 'instore'
        verbose_name = '入库单'
        verbose_name_plural = '入库单'


class OutStore(models.Model):
    
    date = models.DateField(verbose_name='出库日期')
    outNo = models.CharField(max_length=128, unique=True, verbose_name='出库单号')
    toWhere = models.CharField(max_length=128, verbose_name='出库去向')
    store = models.ForeignKey(to=Store, on_delete=models.CASCADE, verbose_name='库存id')
    num = models.IntegerField(verbose_name='数量')
    demount = models.CharField(max_length=128, verbose_name='扣款金额')
    reciTeam = models.CharField(max_length=128, verbose_name='自用/班组')
    receiver = models.CharField(max_length=128, verbose_name='领用人')
    remark = models.TextField(max_length=256, verbose_name='备注', null=True, blank=True)
    
    def __str__(self):
        return '[%s]' % (self.outNo)
    
    class Meta:
        ordering = ['-date']
        db_table = 'outstore'
        verbose_name = '出库单'
        verbose_name_plural = '出库单'
