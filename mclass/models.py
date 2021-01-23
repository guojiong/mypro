from django.db import models

# Create your models here.
class Mclass(models.Model):
    mtype = models.CharField(max_length=128, verbose_name='材料类别')
    mclass = models.CharField(max_length=128, verbose_name='材料小类')
    content = models.TextField(max_length=256, verbose_name='核算内容', null=True, blank=True)
    remark = models.TextField(max_length=256, verbose_name='备注', null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    def __str__(self):
        return '[%s]_%s' % (self.mtype, self.mclass)
    
    class Meta:
        ordering = ['-create_time']
        db_table = 'mclass'
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def getMtypeDropDownList(self):
        return tuple([(0, '')] + list(Mclass.objects.values_list('mtype', 'mtype').distinct().order_by('mtype')))

    def getMclassDropDownList(self):
        return tuple([(0, '')] + list(Mclass.objects.values_list('mclass', 'mclass').distinct().order_by('mclass')))
