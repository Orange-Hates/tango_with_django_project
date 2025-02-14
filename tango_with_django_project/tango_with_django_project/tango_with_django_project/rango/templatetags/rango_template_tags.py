from django import template
from rango.models import Category  # Import the model

register = template.Library()

@register.inclusion_tag('rango/categories.html')  # FIX: Use a separate categories.html
def get_category_list(current_category=None):
    """
    Returns a dictionary with categories for templates.
    Optionally highlights the current category.
    """
    return {'categories': Category.objects.all(), 'current_category': current_category}
