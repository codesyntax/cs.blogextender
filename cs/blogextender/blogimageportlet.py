from Acquisition import aq_inner
from Acquisition import aq_parent
from .interfaces import IBlog
from zope.interface import implements

from plone.memoize.instance import memoizedproperty
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.i18nmessageid import MessageFactory
__ = MessageFactory("plone")


class IBlogImagePortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IBlogImagePortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u''):
    #    self.some_field = some_field

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return __(u"Portlet with general blog info")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('blogimageportlet.pt')

    @memoizedproperty
    def parentblog(self):
        context = aq_inner(self.context)
        while not IPloneSiteRoot.providedBy(context):
            if IBlog.providedBy(context):
                image = context.restrictedTraverse('@@images').tag('image')
                image_thumb = context.restrictedTraverse('@@images').tag('image', scale='image')
                return {'Title': context.Title(),
                        'absolute_url': context.absolute_url(),
                        'image': image,
                        'image_thumb': image_thumb,
                        'feedburner_posts': context.feedburner_posts,
                        'feedburner_comments': context.feedburner_comments,
                        }
            context = aq_parent(context)

        return {}

    @property
    def available(self):
        """Show the portlet only if there are one or more elements."""
        return bool(self.parentblog)

# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.


class AddForm(base.NullAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    def create(self):
        return Assignment()
