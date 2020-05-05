

class SSHPublicKeyManager(models.Manager):
    def get_queryset(self):
        return super().filter(owner=)

    def authors(self):
        return self.get_queryset().authors()

    def editors(self):
        return self.get_queryset().editors()
