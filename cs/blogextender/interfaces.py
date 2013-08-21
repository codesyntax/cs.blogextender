from zope.interface import Interface


class ICSBlogExtenderLayer(Interface):
    """A layer specific to my product
    """


class IBlog(Interface):
    """ Marker interface to blogs
    """
