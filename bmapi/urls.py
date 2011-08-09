
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/0.1/', include('bmapi.api.urls')),

    url(r'^accounts/profile/create/$',
        'profiles.views.create_profile',
        name='profiles_create_profile'),

    url(r'^accounts/profile/edit/$',
        'profiles.views.edit_profile',
        name='profiles_edit_profile'),

    url(r'^accounts/profile/$',
        'bmprofile.views.my_profile',
        name='profiles_profile_my_detail'),

    url(r'^accounts/profile/(?P<username>\w+)/$',
        'bmprofile.views.my_profile',
        name='profiles_profile_detail'),

    url(r'^accounts/', include('registration.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

