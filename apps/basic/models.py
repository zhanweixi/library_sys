# -*-coding:UTF-8-*-
from django.db import models

class LogMsg(models.Model):
    '''系统日志模型定义'''
    asctime = models.CharField(verbose_name="日志时间", max_length=250, null=True, blank=True)
    pathname = models.CharField(verbose_name="文件路径", max_length=250, null=True, blank=True)
    filename = models.CharField(verbose_name="文件名称", max_length=100, null=True, blank=True, db_index=True)
    funcName = models.CharField(verbose_name="函数名", max_length=100, null=True, blank=True, db_index=True)
    line_no = models.IntegerField(verbose_name="行号", null=True, blank=True, default=0)
    levelname = models.CharField(verbose_name="日志级别", max_length=50, null=True, blank=True, db_index=True)
    message = models.TextField(verbose_name="日志内容", null=True, blank=True)
    remark = models.TextField(verbose_name="备注", null=True, blank=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '系统日志信息表'
        verbose_name_plural = '系统日志信息表'

    def short_remark(self):
        if len(str(self.remark)) > 100:
            return '{}...'.format(str(self.remark)[0:100])
        else:
            return str(self.remark)

    short_remark.allow_tags = True
    short_remark.short_description = '备注内容'
