from five import grok
from zope.interface import Interface

from Acquisition import aq_inner, aq_parent

from ..interfaces import IBlog
from Products.CMFPlone.interfaces import IPloneSiteRoot

grok.templatedir('templates')


class ParentBlog(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('parentblog')

    def returnblog(self):
        context = aq_inner(self.context)
        while not IPloneSiteRoot.providedBy(context):
            if IBlog.providedBy(context):
                image = context.restrictedTraverse('@@images').tag('image')
                return {'Title': context.Title(),
                        'absolute_url': context.absolute_url(),
                        'image': image,
                        }

            context = aq_parent(context)

        return None


class ParentBlogHeader(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('parentblogheader')

    def returnblog(self):
        context = aq_inner(self.context)
        self.image = None
        while not IPloneSiteRoot.providedBy(context):
            if IBlog.providedBy(context):
                img_field = context.getField('header_image')
                image = None
                if img_field.get(context):
                    width, height = img_field.getSize(context)
                    image = context.restrictedTraverse('@@images').scale('header_image', width=width, height=height).tag(title=context.Title())
                return {'Title': context.Title(),
                        'absolute_url': context.absolute_url(),
                        'image': image,
                       }

            context = aq_parent(context)

        return None