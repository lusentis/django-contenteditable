from django import template

"""
Builds a beautyful file uploader in pure JS and HTML5
Template tag requires one argument
 - element id in which the player should appear

Usage: {% insert_uploader container-id action-url %}
"""

register = template.Library()

@register.tag(name='insert_uploader')
def do_insert_uploader(parser, token):
    try:
		tag_name, container_id  = token.split_contents()
		return UploaderTemplate(container_id)

    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires one argument" % token.contents.split()[0])

class UploaderTemplate(template.Node):
    def __init__(self, container_id):
		self.container_id = container_id

    def render(self, context):
        return """
    <script type="text/javascript">        
        function createUploader() {{
            var uploader = new qq.FileUploader({{ 
                element: document.getElementById({container_id}),
                action: $uploaderAction,
                debug: false,
		onSubmit: $uploadSubmitCallback,
		onComplete: $uploadSuccessCallback,
		listElement: $listElement
            }});
	}};
        $(function(){
	    createUploader();
	});
    </script>
		""".format(container_id=self.container_id)

