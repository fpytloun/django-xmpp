# -*- coding: utf-8 -*-

from django import template
from ..utils import get_conversejs_context
from django.conf import settings

register = template.Library()


@register.inclusion_tag('conversejs_initialize.html', takes_context=True)
def conversejs_initialize(context):
    return get_conversejs_context(context)


@register.simple_tag
def xmpp_domain():
    return settings.XMPP_DOMAIN


@register.simple_tag
def xmpp_jid(user):
    return '%s@%s' % (user.username.lower(), xmpp_domain())


@register.simple_tag
def xmpp_domain_muc():
    return getattr(settings, 'XMPP_DOMAIN_MUC', 'conference.%s' % settings.XMPP_DOMAIN)
