from django.db import models


class CommonModelMixin(models.Model):
    create_date = models.DateTimeField(verbose_name="创建时间", null=True, blank=True, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    remarks = models.CharField(verbose_name="备注信息", max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
