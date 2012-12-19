from django import template
from django.template.loader import render_to_string
register = template.Library()


class RenderNode(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def render(self, context):
        obj = self.obj.resolve(context)
        tempate_name = obj.get_template()
        return render_to_string(tempate_name, context)


@register.tag
def render_object(parser, token):
    try:
        tag_name, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'render_object tag requires 1 argument (obj), %s given' % \
                    (len(token.split_contents()) - 1)
            )
    return RenderNode(obj)
