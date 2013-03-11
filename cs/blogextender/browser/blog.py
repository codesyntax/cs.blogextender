from zope.interface import Interface
from zope.interface import implements
from Products.statusmessages.interfaces import IStatusMessage
from eibarorg.theme.extenders.interfaces import IBlog
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.utilities.interfaces import IMarkerInterfaces
from Products.CMFCore.utils import getToolByName
from collective.blog.view.adapters import FolderEntryGetter
from collective.blog.view.default_item import DefaultItemView as Base

from cs.blogextender import extenderMessageFactory as _


class BlogEntryGetter(FolderEntryGetter):
    def _base_query(self):
        portal_properties = getToolByName(self.context, 'portal_properties', None)
        site_properties = getattr(portal_properties, 'site_properties', None)
        portal_types = site_properties.getProperty('blog_types', None)
        if portal_types is None:
            portal_types = ('Document', 'News Item', 'File')

        path = '/'.join(self.context.getPhysicalPath())
        return dict(path={'query': path, 'depth': 1},
                    portal_type=portal_types,
                    sort_on='effective',
                    sort_order='reverse',
                    review_state='published')


class DefaultItemView(Base):
    template = ViewPageTemplateFile('templates/blog_item_summary_view.pt')


class BlogActivationHandler(BrowserView):
    def __call__(self, deact=0):
        context = aq_inner(self.context)
        adapted = IMarkerInterfaces(context)
        if not deact:
            adapted.update(add=[IBlog], remove=[])
            message = _('Blog enabled correctly')
            IStatusMessage(self.request).add(message)
        else:
            message = _('Blog disabled correctly')
            IStatusMessage(self.request).add(message)
            adapted.update(add=[], remove=[IBlog])

        return self.request.response.redirect(context.absolute_url())


class IBlogChecker(Interface):
    def isBlog(self):
        """ return wether the context object is a blog """

    def notIsBlog(self):
        """ return wether the context object is not a blog """


class BlogChecker(BrowserView):
    implements(IBlogChecker)

    def isBlog(self):
        """ is blog? """
        context = aq_inner(self.context)
        return IBlog.providedBy(context)

    def notIsBlog(self):
        """ is not blog? """
        return not self.isBlog()
