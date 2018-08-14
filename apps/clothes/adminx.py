# -*- coding:utf-8 -*-
__author__ = 'Cliff Huang'
__date__ = '2018/4/18 1:14'


import xadmin


from .models import *


class FabricAdmin(object):
    pass


class BrandAdmin(object):
    list_display = ['name']


class ClothesAdmin(object):
    list_display = ['name', 'brand','seasons','size_to_styles','fabric','sleeve']
    search_fields = ['name', 'brand','fabric','sleeve']
    list_filter = ['name', 'brand','seasons','sleeve','price','sold']


class ColorAdmin(object):
    pass


class SeasonAdmin(object):
    pass


class StyleAdmin(object):
    pass


class SizeToStyleAdmin(object):
    pass


xadmin.site.register(Fabric, FabricAdmin)
xadmin.site.register(Brand, BrandAdmin)
xadmin.site.register(Season, SeasonAdmin)
xadmin.site.register(Style, StyleAdmin)
xadmin.site.register(SizeToStyle, SizeToStyleAdmin)
xadmin.site.register(Clothes, ClothesAdmin)
xadmin.site.register(Color, ColorAdmin)
