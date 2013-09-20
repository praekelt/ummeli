from django import template
from django.template.loader import render_to_string
from reporting import helpers
from django.core.urlresolvers import reverse

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


@register.assignment_tag(takes_context=True)
def get_tasks_for_user(context, campaign):
    request = context['request']
    if campaign:
        tasks = campaign.tasks.filter(taskcheckout__user=request.user,
                                    taskcheckout__state=0)
        if tasks.exists():
            return tasks
    return None


@register.inclusion_tag('opportunities/inclusion_tags/report_warnings.html', takes_context=True)
def opportunity_report_warnings(context, obj, back):
    from ummeli.opportunities.models import UmmeliOpportunity
    scam_votes = helpers.get_object_votes(obj, UmmeliOpportunity.SCAM_REPORT_KEY_FIELD)
    postion_filled_votes = helpers.get_object_votes(obj, UmmeliOpportunity.POSITION_FILLED_REPORT_KEY_FIELD)
    inappropriate_votes = helpers.get_object_votes(obj, UmmeliOpportunity.INAPPROPRIATE_REPORT_KEY_FIELD)

    REPORT_LIMIT = 3

    context['is_scam'] = scam_votes >= REPORT_LIMIT
    context['is_position_filled'] = postion_filled_votes >= REPORT_LIMIT
    obj.is_removed_by_community = inappropriate_votes >= REPORT_LIMIT
    context['object'] = obj
    context['back'] = reverse(back)
    return context


@register.inclusion_tag('opportunities/inclusion_tags/report_links.html', takes_context=True)
def opportunity_report_links(context, obj):
    from ummeli.opportunities.models import UmmeliOpportunity

    context['scam_key'] = UmmeliOpportunity.SCAM_REPORT_KEY_FIELD
    context['inappropriate_key'] = UmmeliOpportunity.INAPPROPRIATE_REPORT_KEY_FIELD
    context['position_filled_key'] = UmmeliOpportunity.POSITION_FILLED_REPORT_KEY_FIELD
    context['object'] = obj
    return context
