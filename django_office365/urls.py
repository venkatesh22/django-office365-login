from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('django_office365.views',
    url(r'^login/$', 'login_begin', name='office365-login'),
    url(r'^complete/$', 'login_complete', name='office365-complete'),
    url(r'^home/$', 'welcome', name='welcome'),
)
urlpatterns += patterns('',
  (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
