from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'update/$', views.UpdateView.as_view(), name="dce_endpoint"),
    url(r'delete/$', 'contenteditable.views.delete_view', {}),
)
