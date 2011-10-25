from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Article(models.Model):
    hash_key = models.CharField(max_length=32,  primary_key = True)
    date = models.DateTimeField(blank=True,  default = datetime.now())
    source = models.CharField(max_length=100)
    text = models.TextField()
    
    def __unicode__(self):  # pragma: no cover
        return '%s - %s - %s' % (self.date,  self.source,  self.text)

class UserSubmittedJobArticle(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(default='')
    moderated = models.BooleanField(default = False)
    date = models.DateTimeField(auto_now_add = True)
    date_updated = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User)
    
    def __unicode__(self):  # pragma: no cover
        return '%s - %s - %s' % (self.date,  self.title,  self.description)
        
    def toViewModel(self):
        class UserSubmittedJobArticleViewModel(object):
            def __init__(self,  user_article):
                self.pk = user_article.pk
                self.source = user_article.title
                self.text = user_article.text
                self.date = user_article.date
                self.user_submitted = True
        return UserSubmittedJobArticleViewModel(self)


class Province(models.Model):
    search_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=45)
    
    def __unicode__(self):  # pragma: no cover
        return self.name

class Category(models.Model):
    hash_key = models.CharField(max_length=32,  primary_key = True)
    title = models.CharField(max_length=45)
    province = models.ForeignKey(Province)
    articles = models.ManyToManyField(Article, blank=True,  null=True)
    user_submitted_job_articles = models.ManyToManyField(UserSubmittedJobArticle, blank=True,  null=True)
    
    def __unicode__(self):  # pragma: no cover
        return self.title
