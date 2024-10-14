import datetime, hashlib, random
from django.db import models

DEFAULT_DATA = (
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz-"  # noqa: 501
)


def md5_id():
    ctime = str(datetime.datetime.now())
    m = hashlib.md5(bytes(''.join(random.sample(DEFAULT_DATA, 21)), encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()


class Md5idField(models.CharField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs["max_length"] = kwargs.pop("max_length", 255)
        kwargs["default"] = md5_id()
        super(Md5idField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['max_length'] = self.max_length
        kwargs.pop('default', None)
        return name, path, args, kwargs