import requests
import logging

LOGGER = logging.getLogger(__name__)


class Pushover():
    """
    pushover notification
    https://pushover.net/
    """

    base_uri = 'https://api.pushover.net'
    port = 443

    def __init__(self, user, token, *args, **kwargs):
        self.user = user
        self.token = token
        self.base_uri = kwargs.pop('base_uri', self.base_uri)
        self.port = kwargs.pop('port', self.port)

    def push(self, message, **kwargs):
        """pushover to the rescue"""
        LOGGER.debug('send pushover notification: user=%s token=%', self.user, self.token)

        url = '{}:{}/1/messages.json'.format(self.base_uri, self.port)

        # parse config
        data =  {
            'user': self.user,
            'token': self.token,
            'message': message
        }
        data.update(kwargs)

        r = requests.post(url, data=data)
        # files = {
        # "attachment": ("image.jpg", open("your_image.jpg", "rb"), "image/jpeg")
        # })
        LOGGER.debug(r.text)
        r.raise_for_status()
        return True