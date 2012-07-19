""" Utility methods for contenteditable """

from django.shortcuts import get_object_or_404


def content_delete(Model, pk):
    obj = get_object_or_404(Model, pk=pk)
    obj.delete()
    return True
