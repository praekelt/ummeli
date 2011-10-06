from django.db import models

class Article(models.Model):
    hash_key = models.CharField(max_length=32,  primary_key = True)
    date = models.CharField(max_length=45)
    source = models.CharField(max_length=100)
    text = models.TextField()
    def __unicode__(self):  # pragma: no cover
        return '%s - %s - %s' % (self.date,  self.source,  self.text)

class Category(models.Model):
    hash_key = models.CharField(max_length=32,  primary_key = True)
    title = models.CharField(max_length=45)
    articles = models.ManyToManyField(Article, blank=True)
    def __unicode__(self):  # pragma: no cover
        return self.title

class Province(models.Model):
    search_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=45)
    job_categories = models.ManyToManyField(Category, blank=True)
    def __unicode__(self):  # pragma: no cover
        return self.name
