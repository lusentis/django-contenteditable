from django.conf import settings

try:
    CONTENTEDITABLE_MODELS = getattr(settings, 'CONTENTEDITABLE_MODELS')
    editable_models = dict(CONTENTEDITABLE_MODELS)
    e_models = dict()
    for appmodel, fields in CONTENTEDITABLE_MODELS:
        app, model = appmodel.split(".")
        e_models[model] = (app, fields)
except AttributeError:
    editable_models = None
    e_models = None

