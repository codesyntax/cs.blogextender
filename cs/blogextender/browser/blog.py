from plone.uuid.interfaces import IUUID
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.constants import CONTEXT_CATEGORY
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from Products.CMFPlone.utils import _createObjectByType
from zope.interface import Interface
from zope.interface import implements
from Products.statusmessages.interfaces import IStatusMessage
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.utilities.interfaces import IMarkerInterfaces
from Products.CMFCore.utils import getToolByName
from collective.blog.view.adapters import FolderEntryGetter
from collective.blog.view.default_item import DefaultItemView as Base
from zope.i18n import translate
from cs.blogextender import extenderMessageFactory as _
from cs.blogextender.interfaces import IBlog
from zope.event import notify
from ..events import BlogEnabled, BlogDisabled
from ..blogimageportlet import Assignment as BIAssignment
from plone.app.portlets.portlets.navigation import Assignment as NavAssignment
from collective.blog.portlets.archive import Assignment as ArAssignment
from Products.ATContentTypes.lib.constraintypes import ENABLED
from collective.portlet.ngcollection.ngcollection import Assignment as NGAssignment

import uuid


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
            self.prepare_blog()
            message = _('Blog enabled correctly')
            notify(BlogEnabled(context))
            IStatusMessage(self.request).add(message)
        else:
            adapted.update(add=[], remove=[IBlog])
            notify(BlogDisabled(context))
            message = _('Blog disabled correctly')
            IStatusMessage(self.request).add(message)

        return self.request.response.redirect(context.absolute_url())

    def prepare_blog(self):
        context = aq_inner(self.context)
        lang = context.Language()
        if 'images' not in context.keys():
            images = _createObjectByType('Folder',
                                context,
                                id='images',
                                title=translate(_(u'Images and files'),
                                                domain='cs.blogextender',
                                                target_language=lang,
                                    ),
                )
            images.setConstrainTypesMode(ENABLED)
            images.setLocallyAllowedTypes(['Image', 'File'])
            images.setExcludeFromNav(True)
            images.reindexObject()
            wstate = getMultiAdapter((images, self.request),
                name=u'plone_context_state').workflow_state()
            if wstate == 'private':
                try:
                    pw = getToolByName(context, 'portal_workflow')
                    pw.doActionFor(images, 'publish')
                except:
                    from logging import getLogger
                    log = getLogger(__name__)
                    log.info('Cannot publish %s' % images.Title())

        if 'replies' not in context.keys():
            replies = _createObjectByType('Collection',
                                context,
                                id='replies',
                                title=_(u'Latest replies'),
                )
            query = [{'i': 'portal_type',
                      'o': 'plone.app.querystring.operation.selection.is',
                      'v': ['Discussion Item']
                      },
                     {'i': 'review_state',
                      'o': 'plone.app.querystring.operation.selection.is',
                      'v': ['published']
                      },
                     {'i': 'path',
                      'o': 'plone.app.querystring.operation.string.path',
                      'v': '/'.join(context.getPhysicalPath())
                      }
                      ]
            replies.setQuery(query)
            replies.setExcludeFromNav(True)
            replies.reindexObject()
            wstate = getMultiAdapter((replies, self.request),
                name=u'plone_context_state').workflow_state()
            if wstate == 'private':
                try:
                    pw = getToolByName(context, 'portal_workflow')
                    pw.doActionFor(replies, 'publish')
                except:
                    from logging import getLogger
                    log = getLogger(__name__)
                    log.info('Cannot publish %s' % replies.Title())
            replies.reindexObject()

        else:
            replies = context.get('replies')

        context.setConstrainTypesMode(ENABLED)
        context.setLocallyAllowedTypes(['News Item'])

        # block portlets
        left_manager = getUtility(IPortletManager,
                                  name='plone.leftcolumn',
                                  context=context,
                                  )
        right_manager = getUtility(IPortletManager,
                                  name='plone.rightcolumn',
                                  context=context,
                                  )
        left_blacklist = getMultiAdapter((context, left_manager),
                                        ILocalPortletAssignmentManager)

        right_blacklist = getMultiAdapter((context, right_manager),
                                        ILocalPortletAssignmentManager)

        left_blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)
        right_blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)

        # add portlets
        right_mapping = getMultiAdapter((context, right_manager),
                                        IPortletAssignmentMapping)

        biportlet = BIAssignment()
        purl = getToolByName(context, 'portal_url')
        navportlet = NavAssignment(root='/'.join(purl.getRelativeContentPath(context)))
        archiveportlet = ArAssignment()
        ngcollection = NGAssignment(
            header=translate(_(u'Latest comments'),
                            domain='cs.blogextender',
                            target_language=lang
                            ),
            target_collection='/'.join(replies.getPhysicalPath()[2:]),
            limit=10,
            show_more=False,
            show_dates=True,
            template='cs.blogextender.browser-portlet-templates:comments_template.pt'
            )

        right_mapping[str(uuid.uuid1())] = biportlet
        right_mapping[str(uuid.uuid1())] = navportlet
        right_mapping[str(uuid.uuid1())] = ngcollection
        right_mapping[str(uuid.uuid1())] = archiveportlet


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