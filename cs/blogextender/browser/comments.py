from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from plone.app.discussion.browser.comments import CommentsViewlet as Base
from plone.app.discussion.interfaces import IConversation

import hashlib
import urllib


class CommentsViewlet(Base):
    def get_gravatar_url(self, reply):
        pps = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal_url = pps.portal().absolute_url()
        default = portal_url + '/defaultUser.gif'
        size = 32
        email = getattr(reply, 'email', '')
        gravatar_url = 'http://www.gravatar.com/avatar/' + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return gravatar_url

    def get_replies(self, workflow_actions=False):
        context = aq_inner(self.context)
        conversation = IConversation(context)
        wf = getToolByName(context, 'portal_workflow')
        def replies_with_workflow_actions():
            # Generator that returns replies dict with workflow actions
            for comment_obj  in conversation.getComments():

                # list all possible workflow actions
                actions = [a for a in wf.listActionInfos(object=comment_obj)
                               if a['category'] == 'workflow' and a['allowed']]

                yield {'comment': comment_obj,
                       'actions': actions}

        if len(conversation.objectIds()) > 0:
            return replies_with_workflow_actions()

        return []
