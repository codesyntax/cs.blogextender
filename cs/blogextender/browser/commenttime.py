from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from five import grok

from plone.app.discussion.interfaces import IComment


class CommentTime(grok.View):
    grok.context(IComment)
    grok.require('zope2.View')
    grok.name('commenttime')

    def render(self):
        created = self.request.get('created', False)
        util = getToolByName(self.context, 'translation_service')
        if created:
            zope_time = DateTime(self.context.creation_date.isoformat())
        else:
            zope_time = DateTime(self.context.modification_date.isoformat())
        return util.toLocalizedTime(zope_time, long_format=True)
