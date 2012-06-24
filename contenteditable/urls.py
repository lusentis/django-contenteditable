from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'update/$', views.UpdateView.as_view()),
    url(r'delete/$', 'contenteditable.views.delete_view', {}),
)
