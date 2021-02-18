from django.db import models


# Create your models here.
class Project(models.Model):
    code = models.CharField(max_length=128, unique=True, verbose_name='项目编号')
    name = models.CharField(max_length=128, unique=True, verbose_name='项目名称')
    remark = models.TextField(max_length=256, verbose_name='备注')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.CharField(max_length=1, unique=True, verbose_name='是否删除')
    
    def __str__(self):
        return '[%s]' % self.name
    
    class Meta:
        ordering = ['-create_time']
        db_table = 'project'
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def getProjectDropDownList(self):
        return tuple([(0, '')] + list(Project.objects.values_list('id', 'name').distinct()))
