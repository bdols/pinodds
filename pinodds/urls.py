from django.conf.urls import patterns, include, url
from pinodds import settings 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinodds.views.home', name='home'),
    # url(r'^pinodds/', include('pinodds.foo.urls')),

    url(r'^table/', 'odds.views.table', name='table'),
    url(r'^bet/', 'odds.views.bet', name='bet'),
    url(r'^tickets/(?P<userid>[0-9+]+)$', 'odds.views.tickets', name='tickets'),
    url(r'^ticket/(?P<ticket_id>[0-9+]+)$', 'odds.views.ticket_view', name='ticket_view'),
    #(r'^accounts/login/$', login),
    #(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^last5/$', 'odds.views.last5'),
    (r'^password_change/$', 'django.contrib.auth.views.password_change'),
    (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
    (r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
