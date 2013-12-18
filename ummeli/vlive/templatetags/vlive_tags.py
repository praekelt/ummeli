from django import template
from django.template.defaultfilters import stringfilter
from tidylib import tidy_fragment
from django.conf import settings
from copy import copy
from datetime import datetime
from ummeli.base.models import Banner
from django.db.models import Q, F

register = template.Library()

@register.filter
def list_get(key, value):
    return dict(key)[value]

@register.filter
@stringfilter
def sanitize_html(value):
    from BeautifulSoup import BeautifulSoup, Comment, Tag
    # FIXME: 'None' should never be saved as text
    if value is None:
        return ''

    # allowed tags for a Vodafone Live <CONTAINER type="data" />
    # this doubles up as a translation table. CKEditor does new-ish
    # HTML than Vodafone Live will accept. We have to translate 'em' back
    # to 'i', and 'strong' back to 'b'.
    #
    # NOTE: Order is important since <strong>'s can be inside <p>'s.
    tags = (
        ('em', 'i'), # when creating them in the editor they're EMs
        ('strong', 'b'),
        ('i', 'i'), # when loading them as I's the editor leaves them
        ('b', 'b'), # we keep them here to prevent them from being removed
        ('u', 'u'),
        ('br', 'br'),
        ('p', 'p'),
    )
    valid_tags = [tag for tag,replacement_tag in tags]
    soup = BeautifulSoup(value)

    # remove all comments from the HTML
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # hide all tags that aren't in the allowed list, but keep
    # their contents
    for tag in soup.findAll(True):
        # Vodafone Live allows for no tag attributes
        tag.attrs = []
        if tag.name not in valid_tags:
            tag.hidden = True

    # replace tags with Vlive equivelants
    for element, replacement_element in tags:
        if element is not replacement_element:
            for tag in soup.findAll(element):
                replacement_tag = Tag(soup, replacement_element)
                replacement_tag.insert(0, tag.text)
                tag.replaceWith(replacement_tag)

    xml = soup.renderContents().decode('utf8')
    fragment, errors = tidy_fragment(xml, {
        'char-encoding': 'utf8'
    })

    return fragment \
            .replace('&nbsp;', ' ') \
            .replace('&rsquo;', '\'') \
            .replace('&lsquo;', '\'') \
            .replace('&quot;', '"') \
            .replace('&ldquo;', '"') \
            .replace('&rdquo;', '"') \
            .replace('&ndash;', "-")

def choose_featured_banner(context, category_slug):
    context = copy(context)
    now = datetime.now().time()

    banners = Banner.permitted.filter(
        # in between on & off
        Q(time_on__lte=now, time_off__gte=now) |
        # roll over night, after on, before 24:00
        Q(time_on__lte=now, time_off__lte=F('time_on')) |
        # roll over night, before off, after 24:00
        Q(time_off__gte=now, time_off__lte=F('time_on')) |
        # either time on or time of not specified.
        Q(time_on__isnull=True) | Q(time_off__isnull=True),
        primary_category__slug=category_slug
    ).order_by('?')

    context.update({
        'banner': banners[0] if banners.exists() else None,
        'ROOT_URL': settings.ROOT_URL,
    })
    return context

@register.inclusion_tag('banner/inclusion_tags/vlive_banner.html', takes_context=True)
def render_vlive_banner(context):
    return choose_featured_banner(context, 'vlive-banner')

@register.inclusion_tag('banner/inclusion_tags/homepage_banner.html', takes_context=True)
def render_homepage_banner(context):
    return choose_featured_banner(context, 'homepage-banner')

