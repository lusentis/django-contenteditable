# Django contenteditable #

With django-contenteditable you can easily create Django apps that use the powerful HTML `contenteditable` attribute.
Contenteditable is supported by all non-mobile browsers, including Internet Explorer (see http://caniuse.com/#feat=contenteditable).

With django-contenteditable you can create simple and easy to use admin interfaces to allow your human users to edit/add/delete contents directly where they view them, without a backend site (e.g.: django.contrib.admin).

## Current status ##
**You should wait a few days until I complete this documentation (expecially views doc).**

I'm using this app in many of my projects (I work at http://www.monkeytrip.it) and it works just fine!

## What can django-contenteditable do ##
Currently, django-contenteditable supports:

1.    Adding multi-field content
2.    Adding single field content
3.    Editing multi-field content
4.    One-click editing (checking a single field, etc...) ** work in progress **
5.    Deleting content
6.    Multiple uploading of images and documents via DnD and File API (limited to one uploader per page)

## Requirements ##
- Django
- jQuery (DOM APIs and $.post for AJAX Requests)

## Limitations ##
- File upload uses HTML5 DnD and File API, so its support is (currently) limited to Firefox and Chrome (see http://caniuse.com/#feat=dragndrop and http://caniuse.com/#feat=fileapi).
- Don't expect that File upload works (now or in the future) on mobile devices (iOS, Android, ...).
- The other features should work on any browser supported by jQuery that can do XMLHttpRequest.

## Security ##
Currently we don't check if a user has editable rights when parsing template tags, so the only security is that `$.post` calls fail because of the `@require_login` decorator you **must** put in contenteditable's views.
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

### Saving an image from POST data ###
_views.py_

```python
	""" 
		class MyImageModel(models.Model):
			media = models.FileField(upload_to='my-upload-dir/')
			...
	"""
	i = MyImageModel.objects.create()
	i.media.save('{filename}.jpg'.format(filename=request.GET.get('filename')), _StrChunk(request.raw_post_data), True)
	i.save()
```


In a near future this will be implemented via XMLHttpRequest2 (see http://www.w3.org/TR/XMLHttpRequest2/).

## Getting Started ##
Nothing is magic, for getting things work you must:

1.	Setup this app (**simple**)
2. 	Write handler views (**simple**)
3.	Insert tags in your template files (**very simple**, usually you don't need to write any HTML more than what you already have to display your content)

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
In most of the cases you should only add a `{% editablesomething... %}` tag in the `class` attribute of an HTML element (I suggest using inline elements like `span`s).

- You **must not** use input elements with these tags, it won't work.
- Remember that HTML only allows **one** `class="..."` attribute, so this code won't work:

```django
<span id="something" class="your-class-1 your-class-2" class="{% editablefoo "bar" "baz" %}"></span>
```
- Other attributes (id, style,...) usually doesn't influence the behaviour of django-contenteditable, but it may override your onclick, onfocus, onblur and onchange events.


#### Adding a _insert something and press enter_ field ####
This code displays a span with a placeholder text. 
When the span is blurred and it has some text (not empty and not placeholder) a new element is created and the span value (`.html()`) will be assigned to it's attribute named FIELD_NAME.

```django
<span id="something" class="your-class-1 your-class-2 {% editableitem "ELEMENT_NAME" "-1" "FIELD_NAME" "PLACEHOLDER" %}"></span>
```
* `ELEMENT_NAME` is "what we are going to add" (a more appropriate name should be MODEL_NAME)
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
	<p class="author"><b>Author:</b>
		<span class="{% editableattr "author" "Insert the author..." %}">
			{{ news.author }}
		</span>
	</p>
</div>
```

See _Tag Reference_ below for full documentation.


#### Adding a delete button ####

```django
<a href="#" title="Click to delete this item" class="{% deletebutton "news" news.pk %}">
	<img src="{{ STATIC_URL }}your-icon-folder/delete.png" width="15" height="15">
</a>
```
The `<a>` tag is used only to get a cursor: pointer; automagically.


#### Adding a Drag-n-Drop File Uploader ####
You need a bit of javascript to define:

- where to POST uploaded files
- where to display file list with progress bars
- what to do when a file is submitted
- what to do when a file upload is complete

In this example when all uploads are completed we display a message and refresh the page.
To avoid writing more code and to be implementation-independent (currently uses qqFileUploader but in the future this will change) you should not change names beginning with `$`.

At the top of the template load the `fileuploader` tag library:

```django
{% load fileuploader %}
```

In `<head>` include `fileuploader.js` and, if you like, `fileuploader.css`:

```html
<script type="text/javascript" src="{{ STATIC_URL }}_js/fileuploader.js"></script>
<link rel="stylesheet" type="text/css" src="{{ STATIC_URL }}_css/fileuploader.css" />
```

Write some HTML and JavaScript:

```html
...
<div id="uploaderlist">File list will be displayed here</div>
<div id="droparea">Files dropped in this area will be uploaded</div>
...
<script type="text/javascript">
	// You should define all of these vars
	var $uploaderAction = "/gallery/upload/{{ album.pk }}/";	// where to submit files
	var $listElement = document.getElementById('uploaderlist');	// jQuery $(...) does not work
	var uploadCount = 0;	// upload counter
	var $uploadSubmitCallback = function() {
		uploadCount++;
	}
	var $uploadSuccessCallback = function() {
		uploadCount--;
		if (uploadCount==0) {
			alert('All files have been uploaded. Press OK to continue...');
			setTimeout(reloadPage, 500);	// Wait just to be sure all AJAX calls are complete
		}
	}
</script>
...
```

Insert the uploader's JavaScript

```django
{% insert_uploader "droparea" %}
```

## Views ##




## Tag Reference ##
Coming soon...
