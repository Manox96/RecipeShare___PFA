from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    """Returns True if the value starts with the argument."""
    return str(value).startswith(str(arg))

@register.filter
def filter_by_user(photos, user):
    """Filter photos by user"""
    return [photo for photo in photos if photo.user == user] 