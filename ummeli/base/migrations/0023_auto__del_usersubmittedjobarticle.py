# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    depends_on = (
        ("ummeli.opportunities", "0018_migrate_user_submitted_jobs_to_opportunity_model"),
    )

    def forwards(self, orm):

        # Deleting model 'UserSubmittedJobArticle'
        db.delete_table('base_usersubmittedjobarticle')

        # Removing M2M table for field user_submitted_job_articles on 'Category'
        db.delete_table('base_category_user_submitted_job_articles')


    def backwards(self, orm):

        # Adding model 'UserSubmittedJobArticle'
        db.create_table('base_usersubmittedjobarticle', (
            ('province', self.gf('django.db.models.fields.TextField')(default='')),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_submitted_job_article_user', to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.TextField')(default='')),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('job_category', self.gf('django.db.models.fields.TextField')(default='')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('base', ['UserSubmittedJobArticle'])

        # Adding M2M table for field user_submitted_job_articles on 'Category'
        db.create_table('base_category_user_submitted_job_articles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['base.category'], null=False)),
            ('usersubmittedjobarticle', models.ForeignKey(orm['base.usersubmittedjobarticle'], null=False))
        ))
        db.create_unique('base_category_user_submitted_job_articles', ['category_id', 'usersubmittedjobarticle_id'])


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 8, 21, 19, 28, 109964)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 8, 21, 19, 28, 109875)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'base.article': {
            'Meta': {'object_name': 'Article'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 8, 21, 19, 27, 869278)', 'blank': 'True'}),
            'hash_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'base.category': {
            'Meta': {'object_name': 'Category'},
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['base.Article']", 'null': 'True', 'blank': 'True'}),
            'hash_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Province']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'base.certificate': {
            'Meta': {'object_name': 'Certificate'},
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'base.curriculumvitae': {
            'Meta': {'object_name': 'CurriculumVitae'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'certificates': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Certificate']", 'symmetrical': 'False', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'comment_as_anon': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'connection_requests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'connection_requests'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_of_birth': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'highest_grade': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'highest_grade_year': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Language']", 'symmetrical': 'False', 'blank': 'True'}),
            'nr_of_faxes_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'preferred_skill': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profiles_preferred'", 'null': 'True', 'to': "orm['base.Skill']"}),
            'province': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Reference']", 'symmetrical': 'False', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'show_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_contact_number': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'profiles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['base.Skill']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'telephone_number': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'work_experiences': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.WorkExperience']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'base.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'read_write': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'base.province': {
            'Meta': {'object_name': 'Province'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'search_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'base.reference': {
            'Meta': {'object_name': 'Reference'},
            'contact_no': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'})
        },
        'base.skill': {
            'Meta': {'object_name': 'Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'skill': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'base.workexperience': {
            'Meta': {'object_name': 'WorkExperience'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'end_year': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_year': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['base']
