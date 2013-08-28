from zope.interface import Interface
from zope.component.interfaces import IObjectEvent


class ICSBlogExtenderLayer(Interface):
    """A layer specific to my product
    """


class IBlog(Interface):
    """ Marker interface to blogs
    """


class IBlogEnabled(IObjectEvent):
    """ Event to be fired when a blog is activated
    """


class IBlogDisabled(IObjectEvent):
    """ Event to be fired when a blog is deactivated
    """
