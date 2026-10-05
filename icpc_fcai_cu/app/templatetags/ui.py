from django import template

register = template.Library()

COLORS = ["#2b6aad", "#ad281c", "#b77900"]


@register.filter
def level_color(level_number):
    try:
        return COLORS[int(level_number) % len(COLORS)]
    except (TypeError, ValueError):
        return COLORS[0]
