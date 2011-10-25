# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Article'
        db.create_table('vlive_article', (
            ('hash_key', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 10, 25, 10, 51, 31, 373649), blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('vlive', ['Article'])

        # Adding model 'UserSubmittedJobArticle'
        db.create_table('vlive_usersubmittedjobarticle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')(default='')),
            ('moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('vlive', ['UserSubmittedJobArticle'])

        # Adding model 'Province'
        db.create_table('vlive_province', (
            ('search_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal('vlive', ['Province'])

        # Adding model 'Category'
        db.create_table('vlive_category', (
            ('hash_key', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vlive.Province'])),
        ))
        db.send_create_signal('vlive', ['Category'])

        # Adding M2M table for field articles on 'Category'
        db.create_table('vlive_category_articles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['vlive.category'], null=False)),
            ('article', models.ForeignKey(orm['vlive.article'], null=False))
        ))
        db.create_unique('vlive_category_articles', ['category_id', 'article_id'])

        # Adding M2M table for field user_submitted_job_articles on 'Category'
        db.create_table('vlive_category_user_submitted_job_articles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['vlive.category'], null=False)),
            ('usersubmittedjobarticle', models.ForeignKey(orm['vlive.usersubmittedjobarticle'], null=False))
        ))
        db.create_unique('vlive_category_user_submitted_job_articles', ['category_id', 'usersubmittedjobarticle_id'])


    def backwards(self, orm):
        
        # Deleting model 'Article'
        db.delete_table('vlive_article')

        # Deleting model 'UserSubmittedJobArticle'
        db.delete_table('vlive_usersubmittedjobarticle')

        # Deleting model 'Province'
        db.delete_table('vlive_province')

        # Deleting model 'Category'
        db.delete_table('vlive_category')

        # Removing M2M table for field articles on 'Category'
        db.delete_table('vlive_category_articles')

        # Removing M2M table for field user_submitted_job_articles on 'Category'
        db.delete_table('vlive_category_user_submitted_job_articles')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vlive.article': {
            'Meta': {'object_name': 'Article'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 25, 10, 51, 31, 373649)', 'blank': 'True'}),
            'hash_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'vlive.category': {
            'Meta': {'object_name': 'Category'},
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['vlive.Article']", 'null': 'True', 'blank': 'True'}),
            'hash_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vlive.Province']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'user_submitted_job_articles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['vlive.UserSubmittedJobArticle']", 'null': 'True', 'blank': 'True'})
        },
        'vlive.province': {
            'Meta': {'object_name': 'Province'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'search_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'vlive.usersubmittedjobarticle': {
            'Meta': {'object_name': 'UserSubmittedJobArticle'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['vlive']
