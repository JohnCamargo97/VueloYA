from django import template

register = template.Library()

#Para leer listas en un querydict en el template, y no solo el ultimo valor
@register.filter
def get_list(dictionary, key):
    return dictionary.getlist(key)

#Para el index de un for loop en el template usando forloop.counter
@register.filter
def index(loop_counter):
    return loop_counter - 1