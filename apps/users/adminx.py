# -*- coding:utf-8 -*-
__author__ = 'Cliff Huang'
__date__ = '2018/4/18 1:12'

from.models import *


import xadmin
from xadmin import views


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "唯美后台管理"
    site_footer = "汉正街唯美服饰"
    menu_style = "accordion"


class MobileVerifyRecordAdmin(object):
    pass





xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)


xadmin.site.register(MobileVerifyRecord,MobileVerifyRecordAdmin)

