from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.views import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def contentupdate(Model, **kwargs):
	pass


@csrf_exempt
@require_POST
#@login_required
def update_view(request):
	"""
	request.POST:
		- model
		- id
		- data*
	"""
	if request.POST.get('model')=='organigramma':
		
	else:
		raise ValueError('Unknown model: {0}'.format(request.POST.get('model')))

	return HttpResponse('ok');


@csrf_exempt
#@require_POST
#@login_required
def delete_view(request):
	if request.POST.get('model')=='organigramma':
		o = get_object_or_404(Organigramma, pk=request.POST.get('id'))
		o.delete()
	elif request.POST.get('model')=='storiadecade':
		o = get_object_or_404(StoriaDecade, pk=int(request.POST.get('id').strip()))
		o.delete()
	elif request.POST.get('model')=='storia':
		o = get_object_or_404(Storia, pk=int(request.POST.get('id').strip()))
		o.delete()
	elif request.POST.get('model')=='album':
		o = get_object_or_404(Album, pk=int(request.POST.get('id').strip()))
		o.delete()
	elif request.POST.get('model')=='immagine':
		o = get_object_or_404(Immagine, pk=int(request.POST.get('id').strip()))
		o.delete()
	elif request.POST.get('model')=='rubrica':
		o = get_object_or_404(Rubrica, pk=int(request.POST.get('id').strip()))
		o.delete()
	else:
		raise ValueError('Unknown model in delete: {0}'.format(request.POST.get('model')))

	return HttpResponse('ok')
	

