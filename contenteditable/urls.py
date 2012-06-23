from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'update/$', 'contenteditable.views.update_view', {}),
    url(r'delete/$', 'contenteditable.views.delete_view', {}),
)
