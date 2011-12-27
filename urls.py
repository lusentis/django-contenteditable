from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
import settings

#from contenteditable.views import update_view

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'update/$', 'contenteditable.views.update_view', {}),
	url(r'delete/$', 'contenteditable.views.delete_view', {}),
)


