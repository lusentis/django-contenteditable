from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.views import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.flatpages.models import FlatPage

@csrf_exempt
@require_POST
@login_required
def update(request):
	print request.POST

	section = request.POST.get('section')
	html = request.POST.get('html')
	
	if not section or not html:
		return HttpResponseServerError("Cannot proceed with empty Section Name or HTML")

	page = get_object_or_404(FlatPage, url="/{0}/".format(section))
	page.content = html
	page.save()

	return HttpResponse("Updated #{0} - {1}".format(page.pk, section))

