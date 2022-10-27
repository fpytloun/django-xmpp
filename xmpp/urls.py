from django.urls import re_path
import xmpp.views as views

urlpatterns = [
    re_path(r'^xhr/search/user/$', views.XhrUserSearchView.as_view(), name='xmpp_xhr_user_search'),
    re_path(r'^xhr/autojoin/$', views.XhrAutoJoinView.as_view(), name='xmpp_xhr_autojoin'),
]
