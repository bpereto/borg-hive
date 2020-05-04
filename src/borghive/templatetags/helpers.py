'''
helper functions
'''
from django import template


def humanmegabytes(MB):
   'Return the given megabytes as a human friendly MB, GB, or TB string'

   if not MB:
       return MB

   MB = float(MB)
   GB = float(1024)
   TB = float(GB ** 2)

   if MB < GB:
      return '{0} MB'.format(MB)
   elif GB <= MB < TB:
      return '{0:.2f} GB'.format(MB/GB)
   elif TB <= MB:
      return '{0:.2f} TB'.format(MB/TB)

register = template.Library()
register.filter('humanmegabytes', humanmegabytes)
