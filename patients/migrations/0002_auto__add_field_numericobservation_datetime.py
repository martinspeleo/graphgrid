# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NumericObservation.datetime'
        db.add_column(u'patients_numericobservation', 'datetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 18, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'NumericObservation.datetime'
        db.delete_column(u'patients_numericobservation', 'datetime')


    models = {
        u'patients.numericobservation': {
            'Meta': {'object_name': 'NumericObservation'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patients.NumericObservationType']"}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patients.Patient']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'patients.numericobservationtype': {
            'Meta': {'object_name': 'NumericObservationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'patients.patient': {
            'Meta': {'object_name': 'Patient'},
            'dob': ('django.db.models.fields.DateField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mrn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['patients']