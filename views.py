from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.views import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.flatpages.models import FlatPage

from club.models import Organigramma, Storia, StoriaDecade
from gallery.models import Album, Immagine
from rubriche.models import Rubrica
from laboratori.models import Laboratorio

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
	r = False

	if request.POST.get('model')=='organigramma':
		r = Organigramma.handle_update(
				pk = int(request.POST.get('id').strip()),
				titolo = request.POST.get('titolo').strip(),
				contenuto = request.POST.get('contenuto'),
			)
	elif request.POST.get('model')=='storiadecade':
		r = StoriaDecade.handle_update(
				pk = int(request.POST.get('id').strip()),
				titolo = request.POST.get('titolo'),
				ordine = request.POST.get('ordine'),
			)
	elif request.POST.get('model')=='storia':
		if request.POST.get('decade'):
			decade_obj = StoriaDecade.objects.get(pk=int(request.POST.get('decade').strip()))
			if not decade_obj:
				return HttpResponseServerError("Decade object not found #{0}".format(request.POST.get('decade')))
		else:
			decade_obj = None

		r = Storia.handle_update(
				pk = int(request.POST.get('id').strip()),
				decade = decade_obj,
				anno = request.POST.get('anno'),
				testo = request.POST.get('testo'),
				ordine = request.POST.get('ordine'),
			)
	elif request.POST.get('model')=='album':
		r = Album.handle_update(
				pk = int(request.POST.get('id').strip()),
				titolo = request.POST.get('titolo').strip(),
			)
	elif request.POST.get('model')=='rubrica':
		r = Rubrica.handle_update(
				pk = int(request.POST.get('id').strip()),
				titolo = request.POST.get('titolo'),
				testo = request.POST.get('testo'),
				autore = request.POST.get('autore'),
				evidenza = request.POST.get('evidenza'),
			)
	elif request.POST.get('model')=='laboratorio':
		r = Laboratorio.handle_update(
				pk = int(request.POST.get('id').strip()),
				categoria = request.POST.get('categoria'),
				titolo = request.POST.get('titolo'),
				testo = request.POST.get('testo'),
				immagine = None,
				gallery = None,
				video = None,
			)
	else:
		raise ValueError('Unknown model: {0}'.format(request.POST.get('model')))

	if r:
		return HttpResponse('{0}'.format(r))
	else:
		return HttpResponseServerError('request error')

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
	

