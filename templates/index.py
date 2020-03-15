from django import templates 
register=templates.Library()

@register.filter
def index(indexible,i):
    return indexible[i]