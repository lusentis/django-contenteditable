from django import template

"""
Builds a beautiful file uploader in pure JS and HTML5
Template tag requires two arguments
 - element id in which the player should appear
 - action url

Usage: {% insert_inlineedit_js container-id %}
"""

register = template.Library()

## CSS
@register.tag(name='insert_inlineedit_css')
def insert_inlineedit_css(parser, token):
	return InlineeditCssTemplate()


class InlineeditCssTemplate(template.Node):
    def __init__(self):
		pass

    def render(self, context):
		return """
		<style type="text/css">
			.contenteditable-bold {
				font-weight:bold !important;
			}
			.contenteditable-italic {
				font-style:italic !important;
			}
			.contenteditable-underline {
				text-decoration: underline !important;
			}
			.contenteditable-h1 {
				font-size: 2em !important;
			}
			.contenteditable-h2 {
				font-size: 1.2em !important;
			}
			.toolbox {
				padding: 3px;
				padding-bottom: 2px;
				position: fixed;
				display: none;
				height: 20px;
				min-height:20px;
				width:auto;
				overflow:hidden;
				background-color:#FFFFAA;
				border:1px solid #7a7a3a;
				z-index:9999;
			}
		</style>
		"""

## EditableBox
@register.tag(name='editablebox')
def do_insert_editablebox(parser, token):
	try:
		tag_name, data_model, data_id = token.split_contents()
		return EditableBoxTemplate(data_model, data_id)
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires data_model and data_id arguments" % token.contents.split()[0])

class EditableBoxTemplate(template.Node):
	def __init__(self, data_model, data_id):
		self.data_model = data_model
		self.data_id = template.Variable(data_id)
	
	def render(self, context):
		if not '{0}'.format(self.data_id).startswith('"'):
			self.data_id = self.data_id.resolve(context)
		return """editablebox\" data-model={0} data-id={1} """.format(self.data_model, self.data_id)

## EditableAttr
@register.tag(name='editableattr')
def do_insert_editableattr(parser, token):
	try:
		tag_name, data_name, data_placeholder = token.split_contents()
		return EditableAttrTemplate(data_name, data_placeholder)
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires data_name and data_placeholder arguments" % token.contents.split()[0])

class EditableAttrTemplate(template.Node):
	def __init__(self, data_name, data_placeholder):
		self.data_name = data_name
		self.data_placeholder = data_placeholder
	
	def render(self, context):
		return """editable clearonclick\" data-name={0} data-placeholder={1} """.format(self.data_name, self.data_placeholder)

## EditableItem
@register.tag(name='editableitem')
def do_editableitem(parser, token):
	try:
		tag_name, data_model, data_id, data_name, data_placeholder = token.split_contents()
		return EditableItemTemplate(data_model, data_id, data_name, data_placeholder)
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires data_model, data_id, data_name, data_placeholder arguments" % toke.contents.split()[0])

class EditableItemTemplate(template.Node):
	def __init__(self, data_model, data_id, data_name, data_placeholder):
		self.data_model = data_model
		self.data_id = template.Variable(data_id)
		self.data_name = data_name
		self.data_placeholder = data_placeholder
	
	def render(self, context):
		if not '{0}'.format(self.data_id).startswith('"'):
			self.data_id = self.data_id.resolve(context)
	
		return """editableitem clearonclick returnsaves\" data-model={0} data-id={1} data-name={2} data-placeholder={3} """.format(
			self.data_model, self.data_id, self.data_name, self.data_placeholder
		)

## DeleteButton
@register.tag(name='deletebutton')
def do_deletebutton(parser, token):
	try:
		tag_name, data_model, data_id = token.split_contents()
		return DeleteButtonTemplate(data_model, data_id)
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires data_model, data_id arguments and data_id must resolve in context." % toke.contents.split()[0])

class DeleteButtonTemplate(template.Node):
	def __init__(self, data_model, data_id):
		self.data_model = data_model
		self.data_id = template.Variable(data_id)

	def render(self, context):
		data_id = self.data_id.resolve(context)
	
		return """deletebutton\" data-model={0} data-id={1} """.format(
			self.data_model, data_id
		)


## JS
@register.tag(name='insert_inlineedit_js')
def do_insert_inlineedit(parser, token):
    try:
		tag_name, container_id = token.split_contents()
		return InlineeditTemplate(container_id)

    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires one argument" % token.contents.split()[0])

class InlineeditTemplate(template.Node):
    def __init__(self, container_id):
		self.container_id = container_id

    def render(self, context):
        return """
		<script type="text/javascript" src="{static_prefix}_js/rangy-core.js"></script>
		<script type="text/javascript" src="{static_prefix}_js/rangy-cssclassapplier.js"></script>
		<script type="text/javascript">
    		var cssApplier;
	    	$(function() {{
        		rangy.init();
   	    	}})
						
			var applySpan = function(suffix) {{
				rangy.createCssClassApplier("contenteditable-"+suffix, {{normalize: true}}).toggleSelection();
			}}
			
			var applyLink = function() {{
				var url = prompt("Indirizzo di destinazione del link:");
				if (!url) {{ return false; }}
				rangy.createCssClassApplier("contenteditable-link", {{
                    elementTagName: "a",
                    elementProperties: {{
                        href: url
                    }}
				}}).toggleSelection();
			}}
		</script>
		<script type="text/javascript">
			$(function(){{
				//Adds toolbox
				$('body').append("<div class=\\"toolbox\\" id=\\"toolboxel\\"><a href=\\"#\\" onclick=\\"applySpan('bold'); return false\\"><img src=\\"{static_prefix}_imgs/toolbaricons/text_bold.png\\" /></a><a href=\\"#\\" onclick=\\"applySpan('italic'); return false\\"><img src=\\"{static_prefix}_imgs/toolbaricons/text_italic.png\\" /></a><a href=\\"#\\" onclick=\\"applySpan('underline'); return false\\"><img src=\\"{static_prefix}_imgs/toolbaricons/text_underline.png\\" /></a><a href=\\"#\\" onclick=\\"applySpan('h1'); return false\\"><img src=\\"{static_prefix}_imgs/toolbaricons/text_heading_1.png\\" /></a><a href=\\"#\\" onclick=\\"applySpan('h2'); return false\\"><img src=\\"{static_prefix}_imgs/toolbaricons/text_heading_2.png\\" /></a><a href=\\"#\\" onclick=\\"applyLink(); return false\\"><img src=\\"{static_prefix}_imgs/toolbaricons/link.png\\" /></a></div>");

				$({container_id}).click(function(){{
					$('#toolboxel').css({{top: $(this).position().top, left: ($(this).position().left+$(this).width())-$('#toolboxel').width()}}).show();
					/*$(this).blur(function() {{
						$('#toolboxel').hide();
					}});*/
				}});
			}});
		</script>
		""".format(static_prefix=context['STATIC_URL'], container_id=self.container_id)

