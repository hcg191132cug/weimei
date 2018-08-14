from django import template

register = template.Library()
# -*- coding:utf-8 -*-
__author__ = 'Cliff Huang'
__date__ = '2018/4/28 15:28'


def clothesReplaceBig(value,arg):
    return value.replace('big',arg)

register.filter('clothesReplaceBig', clothesReplaceBig)