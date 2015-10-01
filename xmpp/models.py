from django.db import models
from django.conf import settings
import datetime
import uuid

from .client import XMPPConnection
from django.utils import timezone

try:
    from django_gravatar.helpers import get_gravatar_url, has_gravatar
    gravatar_available = True
except ImportError:
    gravatar_available = False

import urllib

import logging
lg = logging.getLogger(__name__)


class XMPPAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='xmpp')
    jid = models.CharField(max_length=300)
    password = models.CharField(max_length=1024)
    created = models.DateTimeField('created', auto_now_add=True)
    updated = models.DateTimeField('updated', blank=True, null=True)

    def __unicode__(self):
        return u'{0}/{1}'.format(self.user, self.jid)

    @staticmethod
    def get_or_create(user):
        """
        Get existing account or create it
        """
        try:
            xmpp_account = XMPPAccount.objects.get(user=user)
        except XMPPAccount.DoesNotExist:
            # Need to generate XMPPAccount object with password that will be later
            # used by ejabberd to authenticate webapp
            xmpp_jid = '%s@%s' % (user.username.lower(), settings.XMPP_DOMAIN)
            # get a random uuid as password
            xmpp_password = uuid.uuid4().hex
            xmpp_account = XMPPAccount.objects.create(jid=xmpp_jid,
                                                      password=xmpp_password,
                                                      user=user)
            xmpp_account.save()

        xmpp_account.update_vcard()
        return xmpp_account

    def update_vcard(self, force=False):
        """
        Update vcard if not updated within `XMPP_UPDATE_VCARD_HOURS` (default False)
        or if XMPP_UPDATE_VCARD is not False
        """
        if not getattr(settings, 'XMPP_UPDATE_VCARD', True):
            # Never ever update vCard
            return False

        update_delta = getattr(settings, 'XMPP_UPDATE_VCARD_HOURS', False)
        if not update_delta:
            return False

        if not force:
            if self.updated and self.updated > timezone.now()-datetime.timedelta(hours=update_delta):
                return False

        lg.info("Updating vCard for %s" % self.jid)
        try:
            con = self.get_connection()
            con.set_vcard(self.user.get_full_name() or self.user.username)
            if gravatar_available and has_gravatar(self.user.email):
                try:
                    avatar_data = urllib.urlopen(get_gravatar_url(self.user.email)).read()
                    con.set_avatar(avatar_data, mime_type='image/jpeg')
                except Exception as e:
                    lg.exception("Failed to set XMPP avatar for %s" % self.jid, e)
            con.disconnect()
        except Exception as e:
            lg.exception("Failed to update vCard for %s" % self.jid, e)

        self.updated = timezone.now()
        self.save()

    def get_connection(self):
        return XMPPConnection(self.jid, self.password)


class XMPPAutoJoin(models.Model):
    account = models.ForeignKey(XMPPAccount, related_name='auto_join')
    jid = models.CharField(max_length=300)
    created = models.DateTimeField('created', auto_now_add=True)
