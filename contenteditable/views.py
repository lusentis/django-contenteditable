from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.views import login_required
from django.views.decorators.http import require_POST
from django.views.generic import View

from contenteditable.utils import content_update_from_dict, content_delete

from contenteditablesettings import CONTENTEDITABLE_MODELS


class UpdateView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        model = request.POST.get('model')
        if CONTENTEDITABLE_MODELS.get(model) is None:
            raise ValueError('Unknown model: {0}'.format(request.POST.get('model')))
        if not request.user.has_perm(model):
            # TODO
            return HttpResponseServerError('User does not have permission')
        e_conf = CONTENTEDITABLE_MODELS[model]
        if content_update_from_dict(e_conf[0], request.POST, e_conf[1]):
            return HttpResponse('ok')
        else:
            return HttpResponseServerError('Content cannot be updated')


@require_POST
#@login_required        ### UNCOMMENT THIS!
def delete_view(request):
    model = request.POST.get('model')
    if CONTENTEDITABLE_MODELS.get(model) is not None:
        content_delete(CONTENTEDITABLE_MODELS[model][0], pk=request.POST.get('id'))
        return HttpResponse('ok')
    else:
        raise ValueError('Unknown model: {0}'.format(request.POST.get('model')))
