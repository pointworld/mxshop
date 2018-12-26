#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

__author__ = 'point'
__date__ = '2018-12-26'


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_operation.models import UserFav


@receiver(post_save, sender=UserFav)
def add_user_fav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_nums += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def cancel_user_fav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_nums -= 1
    goods.save()
