from Products.CMFCore.utils import getToolByName
from collective.blog.view.adapters import FolderEntryGetter
from collective.blog.view.default_item import DefaultItemView as Base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


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
