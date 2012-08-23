import json

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.views import login_required
from django.db import models
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from contenteditable.utils import content_delete

from .settings import editable_models, e_models


class NoPermission(Exception):
    message = 'User does not have permission'
    pass


class UpdateView(View, SingleObjectMixin):
    http_method_names = ['post', 'put']  # TODO delete

    def get_editable_model_and_fields(self, data):
        model_name = data.pop('model')
        try:
            if 'app' in data:
                app_name = data.pop('app')
                full_model_name = "%s.%s" % (app_name, model_name)
            else:
                # missing app name, guess it based on the model name
                full_model_name = e_models[model_name]
                app_name = full_model_name.split('.')[0]
            editable_fields = editable_models[full_model_name]
            model = models.get_model(app_name, model_name)
        # TODO except model does not exist
        except KeyError:
            raise ValueError('Unknown model: {0}'.format(model))
        if not self.request.user.has_perm(model):
            raise NoPermission
        return model, editable_fields

    def post(self, request, *args, **kwargs):
        data = request.POST.dict().copy()
        try:
            self.model, editable_fields = self.get_editable_model_and_fields(data)
        except NoPermission as e:
            return HttpResponseForbidden(
                json.dumps(dict(message=e.message)),
                content_type='application/json')
        if 'slugfield' in data:
            self.slug_field = data.pop('slugfield')
        self.kwargs.update(data)
        obj = self.get_object()
        for fieldname in editable_fields:
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
        model, editable_fields = self.get_editable_model_and_fields(data)
        obj_data = {}
        if 'slugfield' in data:
            # inserting stuff that uses slugs probably won't work unless the
            # slug is one of the editable attributes
            slug_field = data.pop('slugfield')
            obj_data[slug_field] = data.pop('slug')
        for fieldname in editable_fields:
            if fieldname in data:
                obj_data[fieldname] = data.pop(fieldname)
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
