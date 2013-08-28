from zope.interface import implements
from zope.component.interfaces import ObjectEvent

from .interfaces import IBlogEnabled
from .interfaces import IBlogDisabled


class BlogEnabled(ObjectEvent):
    implements(IBlogEnabled)


class BlogDisabled(ObjectEvent):
    implements(IBlogDisabled)
