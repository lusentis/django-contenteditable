import json

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.views import login_required
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from contenteditable.utils import content_delete

from contenteditablesettings import CONTENTEDITABLE_MODELS


class UpdateView(View, SingleObjectMixin):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = request.POST.dict().copy()
        model = data.pop('model')
        # TODO: model may not correspond to actual model name
        if CONTENTEDITABLE_MODELS.get(model) is None:
            raise ValueError('Unknown model: {0}'.format(model))
        if not request.user.has_perm(model):
            return HttpResponseForbidden(
                json.dumps(dict(message='User does not have permission')),
                content_type='application/json')
        e_conf = CONTENTEDITABLE_MODELS[model]
        self.model = e_conf[0]
        if 'slugfield' in data:
            self.slug_field = data.pop('slugfield')
        self.kwargs.update(data)
        obj = self.get_object()
        for fieldname in e_conf[1]:
            if fieldname in data:
                obj.__setattr__(fieldname, data.pop(fieldname))
        obj.save()  # TODO only save if changed
        return HttpResponse(
            json.dumps(dict(message='ok')),
            content_type='application/json')
        # else:
        #     return HttpResponseBadRequest(
        #         json.dumps(dict(message='Content cannot be updated')),
        #         content_type='application/json')

    def put(self, request, *args, **kwargs):
        # TODO test this
        data = request.POST.dict().copy()
        model = data.pop('model')
        e_conf = CONTENTEDITABLE_MODELS[model]
        model = e_conf[0]
        obj_data = {}
        if 'slugfield' in data:
            # inserting stuff that uses slugs probably won't work unless the
            # slug is one of the editable attributes
            slug_field = data.pop('slugfield')
            obj_data[slug_field] = data.pop('slug')
        for k in e_conf[1]:
            if k in data:
                obj_data[k] = data.pop(k)
        obj = model.objects.create(**obj_data)
        return HttpResponse(
            json.dumps(dict(message='ok', pk=obj.pk)),
            content_type='application/json')
        pass


@require_POST
#@login_required        ### UNCOMMENT THIS!
def delete_view(request):
    model = request.POST.get('model')
    if CONTENTEDITABLE_MODELS.get(model) is not None:
        content_delete(CONTENTEDITABLE_MODELS[model][0], pk=request.POST.get('id'))
        return HttpResponse('ok')
    else:
        raise ValueError('Unknown model: {0}'.format(request.POST.get('model')))
