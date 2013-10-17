from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


class CommentTime(BrowserView):

    def __call__(self):
        created = self.request.get('created', False)
        util = getToolByName(self.context, 'translation_service')
        if created:
            zope_time = DateTime(self.context.creation_date.isoformat())
        else:
            zope_time = DateTime(self.context.modification_date.isoformat())
        return util.toLocalizedTime(zope_time, long_format=True)
