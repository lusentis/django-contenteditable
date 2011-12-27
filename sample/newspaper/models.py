from django.db import models

class Article(models.Model):
	title = models.CharField(max_length=200)
	text = models.TextField(default='This article has no text', blank=True, null=True)

	def __unicode__(self):
		return "{0}".format(self.title)

