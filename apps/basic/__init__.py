# -*-coding:utf-8-*-
from django.apps import AppConfig

default_app_config = 'apps.basic.BasicConfig'

VERBOSE_APP_NAME = "系统基础模块"


class BasicConfig(AppConfig):
    name = 'apps.basic'
    verbose_name = VERBOSE_APP_NAME