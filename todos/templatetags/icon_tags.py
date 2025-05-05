from django import template
from utils.message_helper import ICON_MAP

register = template.Library()

@register.simple_tag
def get_icon(level):
    return ICON_MAP.get(level, "")
