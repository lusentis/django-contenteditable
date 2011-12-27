# Django contenteditable #

With django-contenteditable you can easily create Django apps that use the powerful HTML contenteditable attribute.
Contenteditable is supported by all mayor browsers, including Internet Explorer (see http://caniuse.com/#feat=contenteditable).

With django-contenteditable you can create simple and easy to use admin interfaces to allow your users to edit/add/delete contents directly without a backend site (e.g.: django.contrib.admin).

## What can django-contenteditable do ##
Currently, django-contenteditable supports:

1.    Adding multi-field content
2.    Adding single field content
3.    Editing multi-field content
4.    One-click editing (checking a single field, etc...)
5.    Deleting content
6.    Multiple uploading of images and documents via DnD and File API.

## Requirements ##
- Django
- jQuery (DOM apis and $.post for AJAX Requests)

## Limitations ##
- File upload uses HTML5 DnD and File API, so its support is (currently) limited to Firefox and Chrome (see http://caniuse.com/#feat=dragndrop and http://caniuse.com/#feat=fileapi).
- Don't expect that File upload works (now or in the future) on mobile devices (iOS, Android, ...)
- The other features should work on any browser supported by jQuery that can do XMLHttpRequest.

## Bugs ##
File uploads are handled as follows:

1.    File is read with FileReader API
2.    File content is stored in a JS variable
3.    The JS variabile is POSTed via XMLHttpRequest

To use the file as the content for a FileField or ImageField you will need a wrapper class that implements a (somewhat) fake .chunks() method.

In a near future I will implement this via XMLHttpRequest2 (see http://www.w3.org/TR/XMLHttpRequest2/).

## How To ##
1.    Clone/download/install django-contenteditable and add `contenteditable` to your `INSTALLED_APPS` setting
2.    Include contenteditable urls
```
urlpatterns += ('',
	(r'contenteditable/(.*)$', include('contenteditable.urls')),
)
```

