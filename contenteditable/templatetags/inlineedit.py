from django import template
from django.db.models import fields
from django.utils.safestring import mark_safe

from ..settings import CONTENTEDITABLE_ENABLED


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
@register.simple_tag
def editablebox(obj):
    if not CONTENTEDITABLE_ENABLED:
        return ''
    data = (
        obj._meta.app_label,
        obj._meta.object_name.lower(),
        obj.pk)
    return 'data-editapp={0} data-editmodel={1} data-editpk={2}'.format(*data)


@register.simple_tag
def editableattr(name, placeholder=""):
    if not CONTENTEDITABLE_ENABLED:
        return ''
    return 'data-editfield="{0}" data-placeholder="{1}" '.format(name, placeholder)


@register.tag(name='editable')
def do_editable(parser, token):
    try:
        bits = token.split_contents()
        if len(bits) == 3:
            tag_name, field, container = token.split_contents()
        else:
            tag_name, field = token.split_contents()
            container = "span"
        objname, fieldname = field.split('.')
    except ValueError as e:
        raise template.TemplateSyntaxError("editable tag expects one argument "
            "formatted like `object.field`, "
            "%s" % e)
    return EditableModelFieldNode(objname, fieldname, container)


class EditableModelFieldNode(template.Node):
    def __init__(self, objname, fieldname, container):
        self.objname = template.Variable(objname)
        self.fieldname = fieldname
        self.container = template.Variable(container)

    def render(self, context):
        try:
            obj = self.objname.resolve(context)
            fieldname = self.fieldname
            field = obj._meta.get_field(fieldname)
            container = self.container.resolve(context)
        except (template.VariableDoesNotExist, fields.FieldDoesNotExist):
            return ''
        attrs = ['data-editfield="%s"' % fieldname,
                 'data-placeholder="%s"' % (field.default if field.default != fields.NOT_PROVIDED else ''),
                 'data-editwidget="%s"' % field.__class__.__name__]
        out = '<{0} {1}>{2}</{0}>'.format(container,
                                          " ".join(attrs),
                                          getattr(obj, fieldname))
        return mark_safe(out)


## EditableItem
@register.tag(name='editableitem')
def do_editableitem(parser, token):
    try:
        tag_name, data_model, data_id, data_name, data_placeholder = token.split_contents()
        return EditableItemTemplate(data_model, data_id, data_name, data_placeholder)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires data_model, data_id, data_name, data_placeholder arguments" % token.contents.split()[0])


class EditableItemTemplate(template.Node):
    def __init__(self, data_model, data_id, data_name, data_placeholder):
        self.data_model = data_model
        self.data_id = template.Variable(data_id)
        self.data_name = data_name
        self.data_placeholder = data_placeholder

    def render(self, context):
        if not CONTENTEDITABLE_ENABLED:
            return ''
        if not '{0}'.format(self.data_id).startswith('"'):
            self.data_id = self.data_id.resolve(context)

        return """editableitem clearonclick returnsaves\" data-model={0} data-id={1} data-name={2} data-placeholder={3} """.format(
            self.data_model, self.data_id, self.data_name, self.data_placeholder
        )


try:
    import chunks  # only expose if chunks is installed

    @register.simple_tag
    def editablechunk(key):
        if not CONTENTEDITABLE_ENABLED:
            return ''
        return ('data-editapp="chunks" data-editmodel="chunk" '
                'data-editslugfield="key"'
                'data-editfield="content" data-editslug="%s"') % key

except ImportError:
    pass


## DeleteButton
@register.tag(name='deletebutton')
def do_deletebutton(parser, token):
    try:
        tag_name, data_model, data_id = token.split_contents()
        return DeleteButtonTemplate(data_model, data_id)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires data_model, data_id arguments and data_id must resolve in context." % token.contents.split()[0])


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
