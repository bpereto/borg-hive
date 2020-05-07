
# pylint: disable=unused-argument

class RepositoryNotCreated(Exception):
    """raise repository not created exception"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, 'Repository is not created, yet')
