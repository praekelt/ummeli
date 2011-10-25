# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Certificate'
        db.create_table('base_certificate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('base', ['Certificate'])

        # Adding model 'Language'
        db.create_table('base_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('readWrite', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('base', ['Language'])

        # Adding model 'WorkExperience'
        db.create_table('base_workexperience', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('startYear', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('endYear', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('base', ['WorkExperience'])

        # Adding model 'Reference'
        db.create_table('base_reference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('contactNo', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
        ))
        db.send_create_signal('base', ['Reference'])

        # Adding model 'CurriculumVitae'
        db.create_table('base_curriculumvitae', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('telephoneNumber', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('streetName', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('highestGrade', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('highestGradeYear', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('dateOfBirth', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('houseNumber', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('nr_of_faxes_sent', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('base', ['CurriculumVitae'])

        # Adding M2M table for field certificates on 'CurriculumVitae'
        db.create_table('base_curriculumvitae_certificates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('curriculumvitae', models.ForeignKey(orm['base.curriculumvitae'], null=False)),
            ('certificate', models.ForeignKey(orm['base.certificate'], null=False))
        ))
        db.create_unique('base_curriculumvitae_certificates', ['curriculumvitae_id', 'certificate_id'])

        # Adding M2M table for field languages on 'CurriculumVitae'
        db.create_table('base_curriculumvitae_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('curriculumvitae', models.ForeignKey(orm['base.curriculumvitae'], null=False)),
            ('language', models.ForeignKey(orm['base.language'], null=False))
        ))
        db.create_unique('base_curriculumvitae_languages', ['curriculumvitae_id', 'language_id'])

        # Adding M2M table for field workExperiences on 'CurriculumVitae'
        db.create_table('base_curriculumvitae_workExperiences', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('curriculumvitae', models.ForeignKey(orm['base.curriculumvitae'], null=False)),
            ('workexperience', models.ForeignKey(orm['base.workexperience'], null=False))
        ))
        db.create_unique('base_curriculumvitae_workExperiences', ['curriculumvitae_id', 'workexperience_id'])

        # Adding M2M table for field references on 'CurriculumVitae'
        db.create_table('base_curriculumvitae_references', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('curriculumvitae', models.ForeignKey(orm['base.curriculumvitae'], null=False)),
            ('reference', models.ForeignKey(orm['base.reference'], null=False))
        ))
        db.create_unique('base_curriculumvitae_references', ['curriculumvitae_id', 'reference_id'])


    def backwards(self, orm):
        
        # Deleting model 'Certificate'
        db.delete_table('base_certificate')

        # Deleting model 'Language'
        db.delete_table('base_language')

        # Deleting model 'WorkExperience'
        db.delete_table('base_workexperience')

        # Deleting model 'Reference'
        db.delete_table('base_reference')

        # Deleting model 'CurriculumVitae'
        db.delete_table('base_curriculumvitae')

        # Removing M2M table for field certificates on 'CurriculumVitae'
        db.delete_table('base_curriculumvitae_certificates')

        # Removing M2M table for field languages on 'CurriculumVitae'
        db.delete_table('base_curriculumvitae_languages')

        # Removing M2M table for field workExperiences on 'CurriculumVitae'
        db.delete_table('base_curriculumvitae_workExperiences')

        # Removing M2M table for field references on 'CurriculumVitae'
        db.delete_table('base_curriculumvitae_references')


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
        'base.certificate': {
            'Meta': {'object_name': 'Certificate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'base.curriculumvitae': {
            'Meta': {'object_name': 'CurriculumVitae'},
            'certificates': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Certificate']", 'symmetrical': 'False', 'blank': 'True'}),
            'dateOfBirth': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'highestGrade': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'highestGradeYear': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'houseNumber': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Language']", 'symmetrical': 'False', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'nr_of_faxes_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Reference']", 'symmetrical': 'False', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'streetName': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'telephoneNumber': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'workExperiences': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.WorkExperience']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'base.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'readWrite': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'base.reference': {
            'Meta': {'object_name': 'Reference'},
            'contactNo': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'})
        },
        'base.workexperience': {
            'Meta': {'object_name': 'WorkExperience'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'endYear': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'startYear': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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
