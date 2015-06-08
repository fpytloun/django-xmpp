import json
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import XMPPAccount


def get_conversejs_settings(settings_dict=None):
    converse_settings = {
        'bosh_service_url': settings.XMPP_BOSH_SERVICE_URL,
        'domain_placeholder': settings.XMPP_DOMAIN,
        'debug': settings.DEBUG,
        'authentication': getattr(settings, 'XMPP_CONVERSEJS_AUTH', 'login'),
        'keepalive': True,
        'auto_login': True,
    }

    try:
        converse_settings.update(settings.XMPP_CONVERSEJS_SETTINGS)
    except AttributeError:
        pass

    if settings:
        converse_settings.update(settings_dict)

    if converse_settings.get('xhr_user_search', None):
        converse_settings['xhr_user_search_url'] = reverse('xmpp_xhr_user_search')

    return converse_settings


def get_conversejs_context(context):
    context['xmpp_enabled'] = settings.XMPP_ENABLED

    if not settings.XMPP_ENABLED:
        # XMPP disabled entirely
        return context

    request = context.get('request')
    if not request.user.is_active:
        # User is not logged in
        return context

    # Setup authentication
    auth_type = getattr(settings, 'XMPP_CONVERSEJS_AUTH', None)
    settings_auth = {}
    if auth_type in ['login', 'prebind']:
        # We need to ensure XMPPAccount for both login and prebind auth
        xmpp_account = XMPPAccount.get_or_create(request.user)
        settings_auth['jid'] = xmpp_account.jid

    if auth_type == 'login':
        settings_auth['password'] = xmpp_account.password
    elif auth_type == 'preauth':
        raise NotImplementedError('preauth is not implemented yet')

    context['conversejs_settings'] = json.dumps(get_conversejs_settings(settings_auth))

    return context
