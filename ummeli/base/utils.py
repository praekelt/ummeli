import cStringIO as StringIO
import ho.pisa as pisa
import re
from django.template.loader import get_template
from django.template import Context


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if pdf.err:
        return None
    return result.getvalue()


def category_from_str(str):
    from ummeli.opportunities.models import CATEGORY_CHOICES
    for key, value in CATEGORY_CHOICES:
        if re.sub('[\s-]', '', value.lower()) == re.sub('[\s-]', '', str.lower()):
            return key
    return 0


def convert_community_job_to_opportunity(community_job, model=None):
    from ummeli.opportunities.models import Job, CATEGORY_CHOICES, Province
    model = model if model else Job
    return model(title=community_job.title,
                 description=community_job.text,
                 category=category_from_str(community_job.job_category),
                 created=community_job.date,
                 modified=community_job.date_updated,
                 publish_on=community_job.date,
                 owner=community_job.user,
                 state='published')
