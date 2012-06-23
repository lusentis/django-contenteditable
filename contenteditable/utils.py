""" Utility methods for contenteditable """

from django.shortcuts import get_object_or_404


def content_update_from_dict(Model, source_dict, keys):
    """
    Updates Model with values from source_dict specified by keys
    """

    if source_dict.get('id') is None:
        raise ValueError('Source dict didn\'t get a value for id.')
    elif source_dict.get('id')=='-1':
        obj = Model()
    else:
        obj = get_object_or_404(Model, pk=source_dict.get('id'))

    for k in keys:
        if k == 'pk': continue  # don't set pkeys
        if source_dict[k] is None: continue # don't set if not passed

        try:
            obj.__setattr__(k, source_dict[k])
        except AttributeError, e:
            raise ValueError('Passed invalid arg `{0}`'.format(k))

    obj.save()
    return obj.pk


def content_delete(Model, pk):
    obj = get_object_or_404(Model, pk=pk)
    obj.delete()
    return True
