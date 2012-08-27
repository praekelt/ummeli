# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Salary'
        db.create_table('opportunities_salary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
            ('frequency', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('opportunities', ['Salary'])

        # Adding model 'Internship'
        db.create_table('opportunities_internship', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
            ('province', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('salary', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['opportunities.Salary'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('opportunities', ['Internship'])

        # Adding model 'Volunteer'
        db.create_table('opportunities_volunteer', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
            ('province', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('salary', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['opportunities.Salary'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('opportunities', ['Volunteer'])

        # Adding model 'Bursary'
        db.create_table('opportunities_bursary', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
            ('province', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('salary', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['opportunities.Salary'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('opportunities', ['Bursary'])

        # Adding model 'Training'
        db.create_table('opportunities_training', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
            ('province', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('salary', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['opportunities.Salary'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal('opportunities', ['Training'])

        # Adding model 'Competition'
        db.create_table('opportunities_competition', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
            ('province', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('salary', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['opportunities.Salary'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal('opportunities', ['Competition'])

        # Adding model 'Event'
        db.create_table('opportunities_event', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
            ('province', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('salary', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['opportunities.Salary'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('opportunities', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Salary'
        db.delete_table('opportunities_salary')

        # Deleting model 'Internship'
        db.delete_table('opportunities_internship')

        # Deleting model 'Volunteer'
        db.delete_table('opportunities_volunteer')

        # Deleting model 'Bursary'
        db.delete_table('opportunities_bursary')

        # Deleting model 'Training'
        db.delete_table('opportunities_training')

        # Deleting model 'Competition'
        db.delete_table('opportunities_competition')

        # Deleting model 'Event'
        db.delete_table('opportunities_event')


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
        'category.category': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'category.tag': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Tag'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'jmbo.modelbase': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'ModelBase'},
            'anonymous_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'anonymous_likes': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'comments_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comments_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'modelbase_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'likes_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary_modelbase_set'", 'null': 'True', 'to': "orm['category.Category']"}),
            'publish_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publishers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['publisher.Publisher']", 'null': 'True', 'blank': 'True'}),
            'retract_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'unpublished'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'opportunities.bursary': {
            'Meta': {'object_name': 'Bursary'},
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'location': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'province': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.competition': {
            'Meta': {'object_name': 'Competition'},
            'cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'location': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'province': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.event': {
            'Meta': {'object_name': 'Event'},
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'location': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'province': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.internship': {
            'Meta': {'object_name': 'Internship'},
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'location': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'province': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.salary': {
            'Meta': {'object_name': 'Salary'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'opportunities.training': {
            'Meta': {'object_name': 'Training'},
            'cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'location': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'province': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.volunteer': {
            'Meta': {'object_name': 'Volunteer'},
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'location': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'province': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'photologue.photoeffect': {
            'Meta': {'object_name': 'PhotoEffect'},
            'background_color': ('django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}),
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'reflection_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.6'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        'publisher.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'secretballot.vote': {
            'Meta': {'unique_together': "(('token', 'content_type', 'object_id'),)", 'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vote': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['opportunities']