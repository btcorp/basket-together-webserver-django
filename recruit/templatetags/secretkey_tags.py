from django import template
from basket_together.settings import common

secret_values = {
    'GOOGLE_MAP_API_KEY': common.GOOGLE_MAP_API_KEY,
    'DISQUS_WEBSITE_SHORTNAME': common.DISQUS_WEBSITE_SHORTNAME,
    'GOOGLE_ANALYTICS_TRACKING_ID': common.GOOGLE_ANALYTICS_TRACKING_ID,
}

register = template.Library()


@register.simple_tag(name='SECRET_KEY')
def get_secret_keys(key_name):
    return getattr(common, key_name)