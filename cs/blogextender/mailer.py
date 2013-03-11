from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.component import adapts
from plone.app.discussion.interfaces import IComment
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.interface import implements
from collective.contentrules.mailadapter.interfaces import IRecipientsResolver
from .interfaces import IBlog


class BlogCommentMailer(object):
    """ Adapter to resolve recipients when a comment is added
    """
    implements(IRecipientsResolver)
    adapts(IComment)

    def __init__(self, context):
        self.context = context

    def recipients(self):
        context = aq_inner(self.context)
        while not IBlog.providedBy(context):
            if IPloneSiteRoot.providedBy(context):
                return []
            context = aq_parent(context)

        if context.email:
            return context.email

        return []
