from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
import logging

log = logging.getLogger(__name__)

handler500 # Pyflakes

urlpatterns = patterns(
    '',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # url(r'^accounts/profile/create/$',
    #     'profiles.views.create_profile',
    #     name='profiles_create_profile'),

    # url(r'^accounts/profile/edit/$',
    #     'profiles.views.edit_profile',
    #     name='profiles_edit_profile'),

    # url(r'^accounts/profile/$',
    #     'bmprofile.views.my_profile',
    #     name='profiles_profile_my_detail'),

    # url(r'^accounts/profile/(?P<username>\w+)/$',
    #     'bmprofile.views.my_profile',
    #     name='profiles_profile_detail'),

    # url(r'^accounts/', include('registration.urls')),

    url(r'^gallery/(?P<url>.*)$',
        'bmapi.views.smart_proxy',
        {'proxy_server' : 'mediagallery', 'prefix' : '/gallery'}),

    url(r'^events/(?P<url>.*)$',
        'bmapi.views.smart_proxy',
        {'proxy_server' : 'playaevents', 'prefix' : '/events'}),

    url(r'^rideshare/(?P<url>.*)$',
        'bmapi.views.smart_proxy',
        {'proxy_server' : 'rideshare', 'prefix' : '/rideshare'})

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
    log.debug('debug urls')
else:
    log.debug('production urls')


