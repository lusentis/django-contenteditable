from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^contenteditable/', include('contenteditable.urls')),
    url(r'', include('newspaper.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)
