from django.db import models


class EditableContent(models.Model):
    pass


"""class Organigramma(EditableContent):
    class Meta:
        verbose_name_plural = "Organigrammi"
    titolo = models.CharField(max_length=200, blank=True)
    contenuto = models.TextField(blank=True)

    def __unicode__(self):
        return "{0}".format(self.titolo)

    @staticmethod
    def handle_update(pk, titolo, contenuto):
        if pk > 0:
            el = Organigramma.objects.get_or_create(pk=pk)
        else:
            el = Organigramma()

        el.titolo = titolo
        el.contenuto = contenuto
        el.save()

        return el.pk"""

