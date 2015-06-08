from django.conf.urls import url
import xmpp.views as views

urlpatterns = [
    url(r'^xhr/search/user/$', views.XhrUserSearchView.as_view(), name='xmpp_xhr_user_search'),
    url(r'^xhr/autojoin/$', views.XhrAutoJoinView.as_view(), name='xmpp_xhr_autojoin'),
]
