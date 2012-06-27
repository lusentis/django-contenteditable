from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView

from newspaper.models import Article

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Article), name='article_list'),
    url(r'^article/(?P<pk>\d+)/$', DetailView.as_view(model=Article),
        name='article_detail'),
)
