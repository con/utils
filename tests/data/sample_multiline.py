class Storage:
    """A storage class."""

    def upload(
        self,
        name,
        content_type=None,
    ) -> str:
        if name:
            return self.client.call(
                Method='put_object',
            )
