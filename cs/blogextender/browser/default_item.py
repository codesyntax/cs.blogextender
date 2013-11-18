from collective.blog.view.default_item import DefaultItemView as Base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DefaultItemView(Base):

    template = ViewPageTemplateFile("templates/default_item.pt")
