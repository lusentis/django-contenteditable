from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'newspaper.views.article_list', name='article_list'),
	url(r'^article/(?P<article_id>\d+)/$', 'newspaper.views.article_detail', name='article_detail'),
)
