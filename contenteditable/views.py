from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.views import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from contenteditable.utils import content_update, content_delete

from newspaper.models import Article

@csrf_exempt
@require_POST
#@login_required	### UNCOMMENT THIS!
def update_view(request):
	"""
	request.POST contains:
		- model
		- id
		- data*
	"""
	if request.POST.get('model')=='article':
		if not content_update(Article, 
				pk=request.POST.get('id').strip(),
				title=request.POST.get('title'),
				text=request.POST.get('text')):
			return HttpResponseServerError('Content cannot be updated')
	else:
		raise ValueError('Unknown model: {0}'.format(request.POST.get('model')))

	return HttpResponse('ok');


@csrf_exempt
@require_POST
#@login_required	### UNCOMMENT THIS!
def delete_view(request):
	if request.POST.get('model')=='article':
		if not content_delete(Article, pk=request.POST.get('id').strip()):
			return HttpResponseServerError('Delete failed')
	else:
		raise ValueError('Unknown model: {0}'.format(request.POST.get('model')))

	return HttpResponse('ok')
	

