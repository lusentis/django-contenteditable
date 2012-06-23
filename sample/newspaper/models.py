from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(default='This article has no text',
                            blank=True, null=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', (), dict(pk=self.pk))
