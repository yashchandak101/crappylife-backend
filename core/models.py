from django.db import models

class SEOModel(models.Model):
    meta_title = models.CharField(max_length=70, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    canonical_url = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True



from core.utils import generate_slug
from articles.models import Article
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = generate_slug(self)
    super().save(*args, **kwargs)

from core.models import SEOModel

class Article(SEOModel):
    
    # existing fields...
    pass
