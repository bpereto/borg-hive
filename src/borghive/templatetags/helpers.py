'''
helper functions
'''
from django import template

# pylint: disable=no-else-return


def humanmegabytes(MB):
    """Return the given megabytes as a human friendly MB, GB, or TB string"""

    if not isinstance(MB, (int, float)):
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

    return MB

register = template.Library()
register.filter('humanmegabytes', humanmegabytes)
