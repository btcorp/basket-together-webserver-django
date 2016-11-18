from django import template
from basket_together.settings import common, dev, prod

secret_values = {
    'GOOGLE_MAP_API_KEY': common.GOOGLE_MAP_API_KEY,
    'DISQUS_WEBSITE_SHORTNAME': common.DISQUS_WEBSITE_SHORTNAME,
    'GOOGLE_ANALYTICS_TRACKING_ID': common.GOOGLE_ANALYTICS_TRACKING_ID,
}

register = template.Library()


@register.simple_tag(name='SECRET_KEY')
def get_secret_keys(key_name, request=None):
    return secret_values[key_name]