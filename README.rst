===========
django-xmpp
===========

XMPP integration for Django app made simple!

.. attention:: This application is in early development stage. Every help or feedback is appreciated.

Features
--------

- `ConverseJS <https://github.com/jcbrand/converse.js>`_ web chat integration

  - surely best available XMPP web client
  - inspired by `TracyWebTech/django-conversejs <https://github.com/TracyWebTech/django-conversejs>`_

- Support for MUC auto join

- Support for users query

- Ejabberd Django authentication using ejabberd_auth management command

  - inspired by `ffalcinelli/django-ejabberd-bridge <https://github.com/ffalcinelli/django-ejabberd-bridge/blob/master/ejabberd_bridge/management/commands/ejabberd_auth.py>`_

- Single sign on functionality without storing user's credentials
  (requires using ejabberd_auth)

- Set avatar using gravatar and vCard during first login

Installation
------------

Install ``django-xmpp`` via pip::

    pip install django-xmpp

Add ``xmpp`` and ``django_gravatar`` into INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'django_gravatar',
        'xmpp',
    )

Setup most important variables::

    XMPP_DOMAIN = 'example.com'
    XMPP_BOSH_SERVICE_URL = 'https://xmpp.example.com:5280/http-bind'

Optionally setup ConverseJS to suit your needs::

    XMPP_CONVERSEJS_SETTINGS = {
        'allow_contact_removal': False,
        'allow_contact_requests': True,
        'auto_subscribe': True,
        'allow_logout': False,
        'allow_muc': True,
        'allow_otr': False,
        'allow_registration': False,
        'message_carbons': True,
        'hide_muc_server': True,
        'use_vcards': True,
        'animate': True,
        'play_sounds': True,
        'xhr_user_search': True,
        'sounds_path': '%ssounds/' % STATIC_URL,
        'visible_toolbar_buttons': {
             'call': False,
             'clear': False,
             'emoticons': True,
             'toggle_participants': False,
        }
    }

Include ``xmpp.urls`` in your ``urls.py``::

    urlpatterns = [
        ...
        url(r'^xmpp/', include("xmpp.urls")),
    ]

Use ConverseJS in your base template::

    {% load xmpp_tags %}
    {% conversejs_initialize %}

Ejabberd Django authentication
------------------------------

Create ``ejaberd_auth.sh`` file that will simply call ``ejabberd_auth``
management command. Adjust to suit your environment (eg. virtualenv)::

    #!/bin/bash
    cd <path_to_your_django_project>
    python manage.py ejabberd_auth $@

Edit ejabberd.yml and add external auth script, eg.::

    host_config:
        "example.com":
            auth_method: external
            extauth_program: "/<path_to_your_project>/ejabberd_auth.sh"

Settings
--------

These are all available settings you may use.

XMPP_BOSH_SERVICE_URL
    URL for ConverseJS BOSH connection

XMPP_DOMAIN
    Default XMPP domain

XMPP_DOMAIN_MUC
    Domain for multi user chats (default converence.<XMPP_DOMAIN>)

XMPP_CONVERSEJS_AUTH
    Authentication type for ConverseJS (prebind is not
    supported so login is the only option)

XMPP_CONVERSEJS_SETTINGS
    dictionary of settings passed to converse.initialize.
    For more list of available options see `Converse.js docs
    <https://conversejs.org/docs/html/configuration.html>`_

XMPP_ENABLED
    Enable or disable XMPP at all

XMPP_UPDATE_VCARD
    Enable or disable vCard update

XMPP_UPDATE_VCARD_HOURS
    Update vCard every n hours (default False)

A note on usernames
-------------------

Jabber IDs are case-insensitive (so "MyUser@domain.com" and "myuser@domain.com" are the same account). By contrast, the ``username`` field in the default Django ``User`` model is case-sensitive (see `this Django ticket <https://code.djangoproject.com/ticket/2273>`_). This means two separate "MyUser" and "myuser" accounts in Django will have the same JID on the XMPP server. The ``ejabberd_auth`` management command will not authenticate such users, and they will both see "Authentication failed" in Converse and other XMPP clients.

To avoid such conflicts, it is recommended to use a custom ``User`` model that enforces unique lowercase usernames with a ``RegexField``. Other characters not allowed in a Jabber ID should be excluded as well. See `this guide <http://archive.jabber.org/userguide/#register>`_ for details.
