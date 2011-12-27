from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from newspaper.models import Article

def article_list(request):
	articles = Article.objects.all()
	return render_to_response('index.html', {'articles': articles}, context_instance=RequestContext(request))

def article_detail(request, article_id):
	article = get_object_or_404(Article, pk=article_id)
	return render_to_response('article.html', {'article': article}, context_instance=RequestContext(request))

