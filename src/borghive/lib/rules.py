import logging

import rules

LOGGER = logging.getLogger(__name__)


@rules.predicate
def is_owner(user, obj):
    """is object owned by user"""
    LOGGER.debug('is_owner: user=%s obj=%s', user, obj)
    return obj.owner == user


@rules.predicate
def owned_by_group(user, obj):
    """object is owned by a group which user has"""
    if hasattr(obj, 'group'):
        return any(x in obj.group.all() for x in user.groups.all())
    return False
