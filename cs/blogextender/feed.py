from zope.component import adapts
from zope.interface import implements
from plone.app.discussion.interfaces import IComment
from DateTime import DateTime
from Products.basesyndication.interfaces import IFeedEntry


class CommentFeedEntry:
    implements(IFeedEntry)
    adapts(IComment)

    def __init__(self, context):
        self.context = context

    def getWebURL(self):
        return self.context.absolute_url()

    def getTitle(self):
        return self.context.Title()

    def getDescription(self):
        return self.context.getText()

    def getBody(self):
        return self.context.getText()

    def getXhtml(self):
        return self.context.getText()

    def getUID(self):
        return self.context.getId()

    def getAuthor(self):
        return self.context.Creator()

    def getEffectiveDate(self):
        zope_time = DateTime(self.context.modification_date.isoformat())
        return zope_time

    def getModifiedDate(self):
        return self.getEffectiveDate()

    def getTags(self):
        return []

    def getRights(self):
        return []

    def getEnclosure(self):
        return None
