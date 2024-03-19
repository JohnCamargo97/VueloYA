from django import template

register = template.Library()

@register.filter
def get_list(dictionary, key):
    return dictionary.getlist(key)

@register.filter
def index(loop_counter):
    return loop_counter - 1