from django.utils.text import slugify

def generate_slug(instance, field_name="title"):
    value = getattr(instance, field_name, None)
    if value:
        slug = slugify(value)
        return slug
    return None
