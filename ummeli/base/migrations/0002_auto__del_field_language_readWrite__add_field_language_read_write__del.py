# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('base_language', 'readWrite', 'read_write')
        db.rename_column('base_reference', 'contactNo', 'contact_no')
        db.rename_column('base_workexperience', 'startYear', 'start_year')
        db.rename_column('base_workexperience', 'endYear', 'end_year')
        db.rename_column('base_curriculumvitae', 'telephoneNumber', 'telephone_number')
        db.rename_column('base_curriculumvitae', 'highestGrade', 'highest_grade')
        db.rename_column('base_curriculumvitae', 'firstName', 'first_name')
        db.rename_column('base_curriculumvitae', 'dateOfBirth', 'date_of_birth')
        db.rename_column('base_curriculumvitae', 'highestGradeYear', 'highest_grade_year')
        db.rename_column('base_curriculumvitae', 'houseNumber', 'house_number')
        db.rename_column('base_curriculumvitae', 'streetName', 'street_name')
        db.rename_table('base_curriculumvitae_workExperiences', 'base_curriculumvitae_work_experiences')


    def backwards(self, orm):
        db.rename_column('base_language', 'read_write', 'readWrite')
        db.rename_column('base_reference', 'contact_no', 'contactNo')
        db.rename_column('base_workexperience', 'start_year', 'startYear')
        db.rename_column('base_workexperience', 'end_year', 'endYear')
        db.rename_column('base_curriculumvitae', 'telephone_number', 'telephoneNumber')
        db.rename_column('base_curriculumvitae', 'highest_grade', 'highestGrade')
        db.rename_column('base_curriculumvitae', 'first_name', 'firstName')
        db.rename_column('base_curriculumvitae', 'date_of_birth', 'dateOfBirth')
        db.rename_column('base_curriculumvitae', 'highest_grade_year', 'highestGradeYear')
        db.rename_column('base_curriculumvitae', 'house_number', 'houseNumber')
        db.rename_column('base_curriculumvitae', 'street_name', 'streetName')
        db.rename_table('base_curriculumvitae_work_experiences', 'base_curriculumvitae_workExperiences')

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
            'date_of_birth': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'highest_grade': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'highest_grade_year': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Language']", 'symmetrical': 'False', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'nr_of_faxes_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Reference']", 'symmetrical': 'False', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
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
        'base.reference': {
            'Meta': {'object_name': 'Reference'},
            'contact_no': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'})
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
