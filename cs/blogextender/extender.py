from zope.component import adapts
from zope.interface import implements

from Products.Archetypes import atapi
from plone.app.blob.field import ImageField

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from .interfaces import IBlog

from cs.blogextender import extenderMessageFactory as _


class MyImageField(ExtensionField, ImageField):
    """A trivial field."""


class MySecondImageField(ExtensionField, ImageField):
    """ A trivial second field """


class MyLinesField(ExtensionField, atapi.LinesField):
    """ A lines field """


class MyStringField2(ExtensionField, atapi.StringField):
    """ A string field """


class MyStringField3(ExtensionField, atapi.StringField):
    """ A string field """


class BlogExtender(object):
    adapts(IBlog)
    implements(ISchemaExtender)

    fields = [
        MyImageField("image",
                    required=True,
                    languageIndependent=True,
                    max_size=(225, 55),
                    sizes={
                            'mini': (200, 200),
                            'thumb': (128, 128),
                            'tile':  (64, 64),
                            'icon':  (32, 32),
                            'listing':  (16, 16),
                           },
                    widget=atapi.ImageWidget(
                        label=_(u'Small image'),
                        description=_(u'Upload your small image here. '),
                        show_content_type=False)
                    ),
        MySecondImageField("header_image",
                    required=False,
                    languageIndependent=True,
                    max_size=(870, 150),
                    sizes={'large': (768, 768),
                           'preview': (400, 400),
                           'mini': (200, 200),
                           'thumb': (128, 128),
                           'tile':  (64, 64),
                           'icon':  (32, 32),
                           'listing':  (16, 16),
                           },
                    widget=atapi.ImageWidget(
                        label=_(u'Header image'),
                        description=_(u'Upload the image for the header of your blog'),
                        show_content_type=False)
                    ),

        MyLinesField("email",
                        required=True,
                        widget=atapi.LinesWidget(
                            label=_(u'E-mail'),
                            description=_('E-mail addresses where you will receive the replies of your posts. One per line.')

                            )
                    ),

        MyStringField2("feedburner_posts",
                        required=False,
                        widget=atapi.StringWidget(
                            label=_(u"FeedBurner address for your blog posts"),
                            description=_("If you are using FeedBurner to manage your RSS feeds, enter here the address of your posts' feed")

                            )
                    ),

        MyStringField3("feedburner_comments",
                        required=False,
                        widget=atapi.StringWidget(
                            label=_(u"FeedBurner address for your blog comments"),
                            description=_("If you are using FeedBurner to manage your RSS feeds, enter here the address of your comments' feed")

                            )
                    ),


                ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
