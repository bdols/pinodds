from django.conf.urls import patterns, include, url
from pinodds import settings 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinodds.views.home', name='home'),
    # url(r'^pinodds/', include('pinodds.foo.urls')),

    url(r'^table/', 'odds.views.table', name='table'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
