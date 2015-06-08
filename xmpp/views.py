from django.views.generic import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.contrib.auth.models import User

from .models import XMPPAccount, XMPPAutoJoin

import json


class XhrUserSearchView(View):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        query = self.request.GET.get('q', '')
        users = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
        users_jid = map(lambda user: {
            'id': '%s@%s' % (user.username.lower(), settings.XMPP_DOMAIN),
            'fullname': user.get_full_name() or user.username,
        }, users)

        return HttpResponse(json.dumps(users_jid), 'application/javascript')


class XhrAutoJoinView(View):
    """
    Toggle auto-join to XMPP jid
    """
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        account = XMPPAccount.get_or_create(self.request.user)
        auto_join = account.auto_join.all()
        if auto_join:
            jids = map(lambda join: {
                'jid': join.jid
            }, auto_join)
        else:
            jids = []
        return HttpResponse(json.dumps(jids), 'application/javascript')

    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        """
        Add, remove or toggle auto-join to given jid
        """
        try:
            action = self.request.POST['action']
            if action not in ['add', 'remove', 'toggle']:
                return HttpResponseBadRequest("Unknown action '%s'" % action)
        except KeyError:
            action = 'toggle'

        try:
            jid = self.request.POST['jid']
        except KeyError:
            return HttpResponseBadRequest('Missing data: jid')
        # TODO: check jid name with regex

        account = XMPPAccount.get_or_create(self.request.user)
        msg = None
        try:
            join_obj = XMPPAutoJoin.objects.get(account=account, jid=jid)
            if action in ['remove', 'toggle']:
                join_obj.delete()
                msg = "Auto join to '%s' removed" % jid
        except XMPPAutoJoin.DoesNotExist:
            if action == 'remove':
                msg = "Auto join to '%s' does not exist" % jid
                pass
            elif action in ['add', 'toggle']:
                msg = "Added auto join to '%s'" % jid
                join_obj = XMPPAutoJoin(account=account, jid=jid)
                join_obj.save()

        res = {
            'status': 200,
            'action': action,
            'msg': msg,
        }

        return HttpResponse(json.dumps(res), 'application/javascript')
