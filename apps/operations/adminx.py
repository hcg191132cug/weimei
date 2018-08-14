# -*- coding:utf-8 -*-
__author__ = 'Cliff Huang'
__date__ = '2018/4/30 15:30'


from.models import *


import xadmin

class BannerAdmin(object):
    pass


xadmin.site.register(Banner,BannerAdmin)