# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UmmeliOpportunity'
        db.create_table('opportunities_ummeliopportunity', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
            ('education', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('salary', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['opportunities.Salary'], null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('is_community', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('opportunities', ['UmmeliOpportunity'])

        # Adding M2M table for field province on 'UmmeliOpportunity'
        db.create_table('opportunities_ummeliopportunity_province', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ummeliopportunity', models.ForeignKey(orm['opportunities.ummeliopportunity'], null=False)),
            ('province', models.ForeignKey(orm['opportunities.province'], null=False))
        ))
        db.create_unique('opportunities_ummeliopportunity_province', ['ummeliopportunity_id', 'province_id'])


    def backwards(self, orm):
        
        # Deleting model 'UmmeliOpportunity'
        db.delete_table('opportunities_ummeliopportunity')

        # Removing M2M table for field province on 'UmmeliOpportunity'
        db.delete_table('opportunities_ummeliopportunity_province')


    models = {
        'atlas.city': {
            'Meta': {'ordering': "('name',)", 'object_name': 'City'},
            'coordinates': ('atlas.fields.CoordinateField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.Region']", 'null': 'True', 'blank': 'True'})
        },
        'atlas.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'border': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'coordinates': ('atlas.fields.CoordinateField', [], {'null': 'True', 'blank': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'atlas.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.City']"}),
            'coordinates': ('atlas.fields.CoordinateField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.Country']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['photologue.Photo']", 'null': 'True', 'blank': 'True'})
        },
        'atlas.region': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('country', 'code'),)", 'object_name': 'Region'},
            'border': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'coordinates': ('atlas.fields.CoordinateField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 6, 16, 40, 0, 104523)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 6, 16, 40, 0, 104432)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'category.category': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'category.tag': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Tag'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.Location']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary_modelbase_set'", 'null': 'True', 'to': "orm['category.Category']"}),
            'publish_on': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'publishers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['publisher.Publisher']", 'null': 'True', 'blank': 'True'}),
            'retract_on': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'null': 'True', 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'unpublished'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'opportunities.bursary': {
            'Meta': {'object_name': 'Bursary'},
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'is_community': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['opportunities.Province']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'is_community': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'must_qualify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'place': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['opportunities.Province']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'qualification_instructions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'qualifiers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.competition': {
            'Meta': {'object_name': 'Competition'},
            'cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'is_community': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['opportunities.Province']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.event': {
            'Meta': {'object_name': 'Event'},
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'is_community': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['opportunities.Province']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.internship': {
            'Meta': {'object_name': 'Internship'},
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'is_community': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['opportunities.Province']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.job': {
            'Meta': {'object_name': 'Job'},
            'category': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'is_community': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['opportunities.Province']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.microtask': {
            'Meta': {'object_name': 'MicroTask'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['opportunities.Campaign']"}),
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'hours_per_task': ('django.db.models.fields.PositiveIntegerField', [], {'default': '24'}),
            'is_community': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['opportunities.Province']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'}),
            'users_per_task': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'opportunities.microtaskresponse': {
            'Meta': {'object_name': 'MicroTaskResponse'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reject_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reject_reason': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opportunities.MicroTask']"}),
            'task_checkout': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['opportunities.TaskCheckout']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'opportunities.province': {
            'Meta': {'object_name': 'Province'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'province': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'opportunities.salary': {
            'Meta': {'object_name': 'Salary'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'opportunities.taskcheckout': {
            'Meta': {'object_name': 'TaskCheckout'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opportunities.MicroTask']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'opportunities.tomtomcampaign': {
            'Meta': {'object_name': 'TomTomCampaign', '_ormbases': ['opportunities.Campaign']},
            'campaign_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['opportunities.Campaign']", 'unique': 'True', 'primary_key': 'True'})
        },
        'opportunities.tomtommicrotask': {
            'Meta': {'object_name': 'TomTomMicroTask', '_ormbases': ['opportunities.MicroTask']},
            'category': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'microtask_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['opportunities.MicroTask']", 'unique': 'True', 'primary_key': 'True'}),
            'poi_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'suburb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tel_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tel_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'opportunities.tomtommicrotaskresponse': {
            'Meta': {'object_name': 'TomTomMicroTaskResponse', '_ormbases': ['opportunities.MicroTaskResponse']},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'microtaskresponse_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['opportunities.MicroTaskResponse']", 'unique': 'True', 'primary_key': 'True'}),
            'poi_has_changed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tel_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tel_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'opportunities.training': {
            'Meta': {'object_name': 'Training'},
            'cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'is_community': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['opportunities.Province']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.ummeliopportunity': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'UmmeliOpportunity', '_ormbases': ['jmbo.ModelBase']},
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'is_community': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['opportunities.Province']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'opportunities.volunteer': {
            'Meta': {'object_name': 'Volunteer'},
            'education': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'is_community': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['opportunities.Province']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'salary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['opportunities.Salary']", 'null': 'True', 'blank': 'True'})
        },
        'photologue.photo': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tags': ('photologue.models.TagField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'title_slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
