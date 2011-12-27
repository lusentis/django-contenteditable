""" Utility methods for contenteditable """

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404

def content_update(Model, **kwargs):
	"""
	This method should be used for testing purposes only.
	I don't think using __setattr__ it's a good idea...
	"""
	if kwargs['pk']=='-1':
		obj = Model()
	else:
		obj = get_object_or_404(Model, pk=kwargs['pk'])
	
	for arg in kwargs:
		if arg == 'pk': continue	# don't set pkeys
		if kwargs[arg] is None: continue # don't set if not passed

		try:
			obj.__setattr__(arg, kwargs[arg])
		except AttributeError, e:
			raise ValueError('Passed invalid arg `{0}`'.format(arg))	

	obj.save()
	return obj.pk

def content_delete(Model, pk):
	obj = get_object_or_404(Model, pk=pk)
	obj.delete()
	return True


