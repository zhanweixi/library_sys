# -*-coding:utf-8-*-
from apps.basic.models import LogMsg
from django.contrib import admin

admin.site.site_header = '图书管理'
admin.site.site_title = '图书管理系统'


class LogMsgAdmin(admin.ModelAdmin):
    '''LogMsg模型管理页面配置'''
    list_display = ("id", "asctime", "filename", 'funcName', 'line_no', 'levelname', 'message', 'short_remark',
                    'create_at')  # 在页面显示指定字段
    list_display_links = ("id", 'message', 'short_remark')
    list_per_page = 50
    search_fields = ("filename", 'funcName', 'message', 'short_remark')
    list_filter = ("filename", 'funcName', 'levelname',)
    ordering = ("-create_at",)


    
admin.site.register(LogMsg, LogMsgAdmin)
