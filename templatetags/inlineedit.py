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
		<script type="text/javascript" src="{static_prefix}js/rangy-core.js"></script>
		<script type="text/javascript" src="{static_prefix}js/rangy-cssclassapplier.js"></script>
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
			function contentUpdate(el) {{
				if ($('#main').html()!=window.localStorage['content']) {{
					el.removeAttr('contenteditable');
					$.post('/contenteditable/update/', {{
						'section': el.attr('data-section-name'),
						'html': $('#main').html()
					}}, function(){{
						el.attr('contenteditable', 'true');
					}});
					window.localStorage['content']=$('#main').html();
				}}
			}}
			
			$(function(){{
				//Adds toolbox
				$('body').append("<div class=\\"toolbox\\" id=\\"toolboxel\\"><a href=\\"#\\" onclick=\\"applySpan('bold'); return false\\"><img src=\\"{static_prefix}img/toolbaricons/text_bold.png\\" /></a><a href=\\"#\\" onclick=\\"applySpan('italic'); return false\\"><img src=\\"{static_prefix}img/toolbaricons/text_italic.png\\" /></a><a href=\\"#\\" onclick=\\"applySpan('underline'); return false\\"><img src=\\"{static_prefix}img/toolbaricons/text_underline.png\\" /></a><a href=\\"#\\" onclick=\\"applySpan('h1'); return false\\"><img src=\\"{static_prefix}img/toolbaricons/text_heading_1.png\\" /></a><a href=\\"#\\" onclick=\\"applySpan('h2'); return false\\"><img src=\\"{static_prefix}img/toolbaricons/text_heading_2.png\\" /></a><a href=\\"#\\" onclick=\\"applyLink(); return false\\"><img src=\\"{static_prefix}img/toolbaricons/link.png\\" /></a></div>");

				$({container_id}).click(function(){{
					$('#toolboxel').css({{top: $(this).position().top, left: ($(this).position().left+$(this).width())-$('#toolboxel').width()}}).show();
					$(this).attr('contenteditable', 'true');
					$(this).blur(function() {{
						setTimeout(contentUpdate, 200, $(this)); //Passing parameters does not work in ie _but_ closure alternative brokes $(this) everywhere.
					}});
				}});
			}});
		</script>
		""".format(static_prefix=context['STATIC_PREFIX'], container_id=self.container_id)

