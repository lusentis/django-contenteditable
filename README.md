# Django contenteditable #

With django-contenteditable you can easily create Django apps that use the powerful HTML `contenteditable` attribute.
Contenteditable is supported by all non-mobile browsers, including Internet Explorer (see http://caniuse.com/#feat=contenteditable).

With django-contenteditable you can create simple and easy to use admin interfaces to allow your human users to edit/add/delete contents directly where they view them, without a backend site (e.g.: django.contrib.admin).

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
- jQuery (DOM APIs and $.post for AJAX Requests)

## Limitations ##
- File upload uses HTML5 DnD and File API, so its support is (currently) limited to Firefox and Chrome (see http://caniuse.com/#feat=dragndrop and http://caniuse.com/#feat=fileapi).
- Don't expect that File upload works (now or in the future) on mobile devices (iOS, Android, ...).
- The other features should work on any browser supported by jQuery that can do XMLHttpRequest.

## Security ##
Currently we don't check if a user has editable rights when parsing template tags, so the only security is that $.post calls fails because of the @require_login decorator you **must** put in contenteditable's views.
In the next few days I'll fix this.

## Bugs ##
File uploads are handled as follows:

1.    File is read with FileReader API
2.    File content is stored in a JS variable
3.    The JS variabile is POSTed via XMLHttpRequest

To use the file as the content for a FileField or ImageField you will need a wrapper class that implements a (somewhat) fake .chunks() method.

### StrChunk example class ###
```python
class _StrChunk():
	"""
		Support for streaming base64-encoded content
	"""
	data = None
	size = -1
	
	def __init__(self, data):
		self.data = data
		self.size = len(data)

	def multiple_chunks():
		return True

	def chunks(self):
		return self.data
```


In a near future this will be implemented via XMLHttpRequest2 (see http://www.w3.org/TR/XMLHttpRequest2/).

## How To ##

### Setup ###
1.    Clone/download/install `django-contenteditable` and add `contenteditable` to your `INSTALLED_APPS` setting
3.    Include contenteditable.urls in main `urls.py`

```python
urlpatterns += ('',
	(r'contenteditable/(.*)$', include('contenteditable.urls')),
)
```
4.    Run `./manage.py collectstatic` and include jQuery and `contenteditable.js` in your base template

```html
<head>
	...
	<script type="text/javascript" src="https://url.to.latest/jquery.js"></script>
	<script type="text/javascript" src="{{ STATIC_URL }}_js/contenteditable.js"></script>
</head>
```
5.    Load `inlineedit` template tag library in your templates

```django
{% load inlineedit %}
```

### Templates ###
Generally, you should only add a {% editablesomething... %} tag in the `class` attribute of an HTML element (I suggest using inline elements like `span`s).
You **must not** use input elements with these tags, it won't work.
Remember that HTML only allows **one** `class="..."` attribute, so this code won't work:

```django
<span id="something" class="your-class-1 your-class-2" class="{% editablefoo "bar" "baz" %}"></span>
```
Other attributes (id, style,...) usually doesn't influence the behaviour of django-contenteditable, but it may override your onclick, onfocus, onblur and onchange events.

#### Adding a _insert something and press enter_ field ####

```django
<span id="something" class="your-class-1 your-class-2 {% editableitem "ELEMENT_NAME" "-1" "FIELD_NAME" "PLACEHOLDER" %}"></span>
```
* `ELEMENT_NAME` is "what we are going to add"
* `-1` is the Primary Key of the element we are going to edit. `-1` means _add a new element_
* `FIELD_NAME` is the field in which we'll put content inserted in the span element
* `PLACEHOLDER` is a placeholder text to display where there is not text in the span

#### Adding an edit form with multiple fields ####
Suppose we are in a page that displays a full news article.
With this code you can make title, author and the whole article editable.
```django
<div class="newsarticle {% editablebox "news" news.pk %}">
	<div class="article-date">{{ news.date|date:'F Y' }}</div>
	<h2><span class="left {% editableattr "title" "Insert the title here..." %}">
		{{ news.title|safe }}
	</span></h2>
	<p class="newstext {% editableattr "text" "Insert news text here..." %}" style="height:auto;">
		{{ rubrica.text|safe }} 
	</p>
	<p class="author"><b>Autore:</b>
		<span class="{% editableattr "autore" "Insert the author..." %}">
			{{ news.author }}
		</span>
	</p>
</div>
```




