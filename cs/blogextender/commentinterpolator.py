from zope.component import adapts
from plone.app.discussion.interfaces import IComment
from eibarorg.theme import themeMessageFactory as _
from zope.interface import implements
from plone.stringinterp.adapters import BaseSubstitution as Base
from plone.stringinterp.adapters import UrlSubstitution as BaseUrlSubstitution
from plone.stringinterp.adapters import TitleSubstitution as BaseTitleSubstitution
from plone.stringinterp.adapters import DateSubstitution

from plone.stringinterp.interfaces import IStringInterpolator


class BaseSubstitution(Base):
    implements(IStringInterpolator)


class UrlSubstitution(BaseUrlSubstitution):
    adapts(IComment)

    category = _(u'Discussion Item')
    description = _(u'URL')


class TitleSubstitution(BaseTitleSubstitution):
    adapts(IComment)

    category = _(u'Discussion Item')
    description = _(u'Title')


class CreatedSubstitution(DateSubstitution):
    adapts(IComment)

    category = _(u'Discussion Item')
    description = _(u'Created')

    def safe_call(self):
        return self.formatDate(self.context.creation_date)


class ModifiedSubstitution(DateSubstitution):
    adapts(IComment)

    category = _(u'Discussion Item')
    description = _(u'Modified')

    def safe_call(self):
        return self.formatDate(self.context.modification_date)


class CreatorSubstitution(BaseSubstitution):
    adapts(IComment)

    category = _(u'Discussion Item')
    description = _(u'Creator')

    def safe_call(self):
        return self.context.Creator()


class TextSubstitution(BaseSubstitution):
    adapts(IComment)

    category = _(u'Discussion Item')
    description = _(u'Text')

    def safe_call(self):
        return self.context.getText(targetMimetype='text/plain')
