from django import template

register = template.Library()


@register.filter(name='get')
def get(value, listing):
    return value.filter(listing=listing).first()
    
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)