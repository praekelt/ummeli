from django.db import models

class Article(models.Model):
    date = models.CharField(max_length=45)
    source = models.CharField(max_length=100)
    text = models.TextField()
    def __unicode__(self):  # pragma: no cover
        return '%s - %s' % (self.title,  self.articles.length)

class Category(models.Model):
    title = models.CharField(max_length=45)
    articles = models.ManyToManyField(Article)
    def __unicode__(self):  # pragma: no cover
        return '%s (%s)' % (self.title,  len(self.articles.all()))

class Province(models.Model):
    search_id = models.IntegerField()
    name = models.CharField(max_length=45)
    job_categories = models.ManyToManyField(Category)
    def __unicode__(self):  # pragma: no cover
        return self.name
